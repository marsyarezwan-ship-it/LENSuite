from data.cefr_profiles import CEFR_PROFILES
def build_prompt(
    school_level,
    cefr,
    age,
    skill,
    resource_type,
    topic,
    material_length,
    num_tasks,
    scaffolding,
    output_features,
    grammar,
    vocabulary,
    vocab_target,
    genre,
    register,
    communicative_function,
    objective,
    approach,
    duration,
    context,
    constraints
):
    profile = CEFR_PROFILES.get(cefr, CEFR_PROFILES["B1"])
    topic_text = topic if topic else "Teacher-selected or contextually appropriate"

    scaffolding_text = (
        ", ".join(scaffolding)
        if scaffolding
        else "No additional scaffolding specified"
    )

    output_features_text = (
        ", ".join(output_features)
        if output_features
        else "No additional teacher resources requested"
    )
    age_text = (
        f"aged approximately {age}"
        if age
        else "with an age-appropriate learner profile"
    )

    grammar_text = grammar if grammar else "Not specified"

    vocab_text = (
        vocab_target
        if vocab_target
        else "No specific topic vocabulary specified"
    )

    function_text = (
        communicative_function
        if communicative_function
        else "Not specified"
    )

    objective_text = (
        objective
        if objective
        else "Not specified"
    )

    context_text = (
        context
        if context
        else "Use an appropriate Malaysian English-learning context."
    )

    constraints_text = (
        constraints
        if constraints
        else "No additional classroom constraints specified."
    )

    prompt = f"""
Create an English language teaching resource for
{school_level} learners at CEFR {cefr}, {age_text}.

PRIMARY LANGUAGE SKILL:
{skill}
MATERIAL DESIGN:

Resource type:
{resource_type}

Topic / theme:
{topic_text}

Material length:
{material_length}

Number of tasks/questions:
{num_tasks}

Scaffolding:
{scaffolding_text}

Additional teacher resources:
{output_features_text}

LINGUISTIC LENS:

LEXICAL PROFILE:
{profile["lexical"]}

Teacher-selected vocabulary profile:
{vocabulary}

Teacher-selected vocabulary/topic focus:
{vocab_text}


GRAMMAR & SYNTAX PROFILE:
{profile["grammar_syntax"]}

Teacher-selected target grammar:
{grammar_text}


DISCOURSE PROFILE:
{profile["discourse"]}

Teacher-selected genre:
{genre}


PRAGMATIC PROFILE:
{profile["pragmatics"]}

Teacher-selected register:
{register}

Teacher-selected communicative function:
{function_text}


PEDAGOGICAL REQUIREMENTS:
- Learning objective: {objective_text}
- Teaching approach: {approach}
- Intended lesson duration: {duration} minutes

CONTEXT:
{context_text}

CLASSROOM CONSTRAINTS:
{constraints_text}

Ensure that the language is appropriate for the stated
learner profile and intended proficiency level.

Maintain consistency between vocabulary, grammar,
genre, register, communicative purpose and the
learning objective.

The material must remain subject to teacher review
and adaptation before classroom use.
"""

    return prompt.strip()