import sys

from sltp.models import FeatureModel
from sltp.features import create_model_factory, compute_static_atoms
from . import PYPERPLAN_DIR


def run_pyperplan(pyperplan, domain, instance, heuristic, parameter_generator):
    # Let's fake a pyperplan command-line arguments object so that
    # we don't have to worry about default parameters. We use "gbf" but will override that next.
    args = pyperplan.parse_args([domain, instance])

    # Parse the domain & instance and create a model generator
    problem, model_factory = create_model_factory(domain, instance, parameter_generator)

    static_atoms, _ = compute_static_atoms(problem)

    pyperplan_heuristic = create_pyperplan_heuristic(model_factory, static_atoms, heuristic)

    # And now we inject our desired search and heuristic functions
    args.search = "gbf"
    args.forced_heuristic = pyperplan_heuristic

    # And run pyperplan!
    pyperplan.main(args)


def import_and_run_pyperplan(domain, instance, heuristic, parameter_generator):
    sys.path.insert(0, PYPERPLAN_DIR)
    import pyperplan
    run_pyperplan(pyperplan, domain, instance, heuristic, parameter_generator)
    sys.path = sys.path[1:]


def create_pyperplan_heuristic(model_factory, static_atoms, heuristic):
    """ Create a pyperplan-like concept-based heuristic with the given features and weights"""
    def pyperplan_concept_based_heuristic(state):
        translated = translate_state(state.state)
        translated_with_statics = translated + list(static_atoms)
        model = FeatureModel(model_factory.create_model(translated_with_statics))

        return heuristic.value(model)

    return pyperplan_concept_based_heuristic


def translate_atom(atom):
    assert atom[0] == '(' and atom[-1] == ')'
    return atom[1:-1].split(' ')


def translate_state(state):
    """ Translate a pyperplan-like state into a list with the format required by SLTP's concept denotation processor """
    return [translate_atom(atom) for atom in state]
