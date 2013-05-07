#!/usr/bin/env python
# Prototype Python metadata parser

import re
import collections

class ParseError(ValueError):
    pass

class Requirement(object):
    _re = re.compile(
        r"""(?P<name>\w+)
            (\s*\[(?P<extras>.*)\])?
            (\s*\((?P<version>.+)\))?""",
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
        return cls(name=groups['name'], extras=extras, version=version)

    def __str__(self):
        parts = [self.name]
        if self.extras:
            parts.append("[" + ", ".join(self.extras) + "]")
        if self.version:
            parts.append("(" + str(self.version) + ")")
        return " ".join(parts)

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
