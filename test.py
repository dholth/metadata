import pymeta

def test_req_re():
    requirements = [
            "markupsafe (>=0.9.2)",
            "beaker (>=1.1)",
            "repoze.sphinx.autointerface",
            "sphinx[docs]",
            "coverage[testing, doc]",
            "coverage[testing, doc] ( >= 0.0.1 )",
            "sphinx ( >= 0.0.1, !=2, <= 3 , < 4, == 1, > 0, 7 )",
            ]
    for r in requirements:
        match = pymeta.Requirement._re.match(r)
        if match:
            print match.groupdict()
        print pymeta.Requirement.parse(r)
