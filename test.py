import pymeta
import pprint

requirements = [
        "markupsafe (>=0.9.2)",
        "beaker (>=1.1)",
        "repoze.sphinx.autointerface",
        "sphinx[docs]",
        "coverage[testing, doc]",
        "coverage[testing, doc] ( >= 0.0.1 )",
        "sphinx ( >= 0.0.1, !=2, <= 3 , < 4, == 1, > 0, 7, >0 )",
        ]

requirements_2 = [
        "markupsafe (>=0.9.2)",
        "beaker (>=1.1)",
        "repoze.sphinx.autointerface",
        "sphinx[docs]",
        "coverage[testing, doc]",
        "coverage[doc, brown] ( >= 0.0.1 )",
        "sphinx ( >= 0.0.1, !=2, <= 3 , < 4, == 1, > 0, 7, >0 )",
        ]

requirements_3 = requirements + ["three"]

def test_req_re():
    for r in requirements:
        match = pymeta.Requirement._re.match(r)
        if match:
            print(match.groupdict())
        print(pymeta.Requirement.parse(r))

def test_metadata_1():
    metadata = {
            'metadata-version':'2.0',
            'classifiers':['Python', 'Metadata'],
            'requires':requirements_3,
            'may-requires':[
                {'extra':'foo', 'values':requirements},
                {'condition':'os_name != "armadillo"', 'values':requirements_2},
                ]
            }

    md = pymeta.Metadata()
    md.parse(metadata)

    print("\nParsed metadata:")
    pprint.pprint(dict(md))

    print("\nConcrete requirements:")
    pprint.pprint(list(md.concrete_requirements()))

    print("\nConcrete requirements with extra [foo]:")
    pprint.pprint(list(md.concrete_requirements(extras=("foo",))))
    
    print("\nFlat requirements with extra [foo] and 'armadillo' os:")
    pprint.pprint(md.flat_requirements(md.concrete_requirements(extras=("foo",))))

    print("\nFlat requirements with extra [foo] and 'armadillo' os:")
    pprint.pprint(md.flat_requirements(md.concrete_requirements(extras=("foo",), 
        environment={'os_name':'armadillo'})))

    print("\nFlat requirements with extra [foo] and 'armadillo' os, without unconditional:")
    pprint.pprint(md.flat_requirements(md.concrete_requirements(extras=("foo",), 
        environment={'os_name':'armadillo'},
        include_unconditional=False)))
