#!/usr/bin/env python
# Prototype Python metadata parser

import collections
import itertools
import markerlib
import re

class ParseError(ValueError):
    pass

class Requirement(object):
    _re = re.compile(
        r"""(?P<name>\w+)
            (\s*\[(?P<extras>.*)\])?
            (\s*(\((?P<version>.+)\)|
             (?P<bw_version>(<|<=|>|>=|==|!=).+)))?""",
            re.VERBOSE)

    def __init__(self, name=None, extras=None, version=None):
        self.name = name
        self.version = version
        self.extras = extras

    @classmethod
    def parse(cls, requirement):
        match = cls._re.match(requirement)
        if not match:
            raise ParseError("Invalid requirement", requirement)
        groups = match.groupdict()
        extras = ()
        if groups['extras']:
            extras = tuple(extra.strip() for extra in groups['extras'].split(','))
        version = None
        if groups['version']:
            version = Version.parse(groups['version'])
        elif groups['bw_version']:
            version = Version.parse(groups['bw_version'])
        return cls(name=groups['name'], extras=extras, version=version)

    def __str__(self):
        parts = [self.name]
        if self.extras:
            parts.append("[" + ", ".join(self.extras) + "]")
        if self.version:
            parts.append("(" + str(self.version) + ")")
        return " ".join(parts)

    def __repr__(self):
        return str(self)

VersionPredicate = collections.namedtuple('VersionPredicate', ['op', 'version'])

class Version(object):
    _re = re.compile(
            r"""\s*
            (?P<op>\<|\>|\<=|\>=|==|!=)?\s*
            (?P<version>[^\s]+)\s*$
            """,
            re.VERBOSE)
    
    def __init__(self, predicates):
        self.predicates = predicates

    @classmethod
    def parse(cls, version):
        predicates = []
        for predicate in (p.strip() for p in version.split(',')):
            match = cls._re.match(predicate)
            if not match:
                raise ParseError("Invalid version predicate", predicate)
            groups = match.groupdict()
            op, version = '', None
            if groups['op']:
                op = groups['op']
            version = groups['version']

            predicates.append(VersionPredicate(op, version))

        return cls(predicates)

    def __str__(self):
        return ', '.join(''.join(vp) for vp in self.predicates)

class ListValue(object):
    def __init__(self, subtype):
        self.subtype = subtype

    def parse(self, value):
        assert isinstance(value, list), value
        items = [self.subtype.parse(item) for item in value]
        return items

class Conditional(object):
    def __init__(self, subtype):
        self.subtype = subtype

    def parse(self, value):
        assert isinstance(value, dict), value
        value['values'] = [self.subtype.parse(v) for v in value['values']]
        value['condition'] = markerlib.compile(value.get('condition', ''))
        return value

class Verbatim(object):
    def __init__(self):
        pass

    def parse(self, value):
        return value

class Metadata(collections.OrderedDict):
    """Typed Python distribution metadata."""
    _parsers = {
            'requires':ListValue(Requirement).parse,
            'may-requires':ListValue(Conditional(Requirement)).parse
            }

    def parse(self, untyped):
        for key in untyped:
            self[key] = self._parsers.get(key, lambda x: x)(untyped[key])

    def concrete_requirements(self, extras=(), environment=None, 
            include_unconditional=True):
        unconditional = ()
        if include_unconditional and 'requires' in self:
            unconditional = ({'values':self['requires']},)
        return itertools.chain(
            (r for r in self['may-requires'] 
                if r['condition'](environment) 
                and ((not r.get('extra')) or r['extra'] in extras)),
            unconditional)

    def flat_requirements(self, concrete):
        """Return a flattened list of requirements without duplicates."""
        by_name = collections.defaultdict(list)
        for group in concrete:
            for r in group['values']:
                by_name[r.name].append(r)
        flat = []
        for name, requirements in by_name.items():
            all_extras = set()
            all_version_predicates = set()
            for r in requirements:
                all_extras.update(r.extras)
                if r.version:
                    all_version_predicates.update(r.version.predicates)
            version = None
            if all_version_predicates:
                version = Version(sorted(all_version_predicates))
            flat.append(Requirement(name=name, extras=sorted(all_extras), version=version))
        return flat

