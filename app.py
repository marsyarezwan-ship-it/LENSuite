import streamlit as st



from modules.lens_engine import build_prompt



from modules.langmri_engine import analyse_text



from modules.flag_engine import (



    evaluate_grammar_target,



    evaluate_discourse,



    evaluate_requested_components,



    evaluate_lexical_frequency



)



from modules.lexical_engine import (



    analyse_lexical_frequency



)



# ============================================================



# PAGE CONFIGURATION



# ============================================================



st.set_page_config(



    page_title="LENSuite ELT",



    page_icon="🔎",



    layout="wide"



)



# ============================================================



# SESSION STATE



# ============================================================



if "page" not in st.session_state:



    st.session_state.page = "home"


# VISUAL SYSTEM
st.markdown("""<style>
:root{--ink:#172033;--muted:#64748B;--primary:#4F46E5;--soft:#EEF2FF;--border:#E2E8F0;--bg:#F8FAFC}
.stApp{background:var(--bg)} .block-container{max-width:1180px;padding-top:4.25rem;padding-bottom:4rem}
h1,h2,h3{color:var(--ink);letter-spacing:-.02em} p,label,.stCaption{color:var(--muted)}
div[data-testid="stButton"]>button{border-radius:12px;min-height:44px;font-weight:650;border:1px solid var(--border)}
div[data-testid="stButton"]>button[kind="primary"]{background:var(--primary);border-color:var(--primary);color:#FFFFFF !important}
div[data-testid="stButton"]>button[kind="primary"] p,
div[data-testid="stButton"]>button[kind="primary"] span{color:#FFFFFF !important}
div[data-testid="stButton"]>button:not([kind="primary"]){color:#334155 !important}
div[data-testid="stButton"]>button:not([kind="primary"]) p,
div[data-testid="stButton"]>button:not([kind="primary"]) span{color:#334155 !important}
div[data-testid="stButton"]>button{transition:background-color .18s ease,border-color .18s ease,color .18s ease,transform .18s ease,box-shadow .18s ease}
div[data-testid="stButton"]>button[kind="primary"]:hover{background:#3730A3 !important;border-color:#3730A3 !important;transform:translateY(-1px);box-shadow:0 7px 16px rgba(79,70,229,.18)}
div[data-testid="stButton"]>button[kind="primary"]:hover p,
div[data-testid="stButton"]>button[kind="primary"]:hover span{color:#FFFFFF !important}
div[data-testid="stButton"]>button:not([kind="primary"]):hover{background:#EEF2FF !important;border-color:#A5B4FC !important;color:#3730A3 !important;transform:translateY(-1px);box-shadow:0 5px 12px rgba(79,70,229,.10)}
div[data-testid="stButton"]>button:not([kind="primary"]):hover p,
div[data-testid="stButton"]>button:not([kind="primary"]):hover span{color:#3730A3 !important}
div[data-testid="stMetric"]{background:white;border:1px solid var(--border);border-radius:14px;padding:.9rem 1rem}
.lens-brand{display:flex;align-items:center;gap:.75rem;margin-bottom:1.35rem}.lens-mark{width:42px;height:42px;border-radius:13px;display:flex;align-items:center;justify-content:center;background:var(--primary);color:white;font-weight:800}.lens-brand-name{color:var(--ink);font-size:1.05rem;font-weight:800}.lens-brand-sub{color:var(--muted);font-size:.75rem}
.lens-flow{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;background:white;border:1px solid var(--border);border-radius:16px;padding:.6rem;margin-bottom:1.8rem}.lens-step{padding:.72rem .85rem;border-radius:11px;color:var(--muted)}.lens-step.active{background:var(--soft);color:#3730A3}.lens-step.done{color:#334155}.lens-step-num{font-size:.68rem;font-weight:800;letter-spacing:.08em}.lens-step-name{font-size:.9rem;font-weight:750;margin-top:.16rem}
.lens-hero{background:linear-gradient(135deg,#FFFFFF 0%,#F5F3FF 100%);border:1px solid #E0E7FF;border-radius:24px;padding:3rem;margin:.4rem 0 1.6rem;box-shadow:0 12px 35px rgba(79,70,229,.07)}.lens-kicker{color:var(--primary);font-size:.78rem;font-weight:800;letter-spacing:.12em}.lens-hero h1{color:#172033 !important;font-size:3rem;line-height:1.08;margin:.65rem 0 1rem;font-weight:800;letter-spacing:-.035em}.lens-hero p{color:#526079 !important;max-width:760px;font-size:1.08rem;line-height:1.65;margin:0}
.lens-card{background:white;border:1px solid var(--border);border-radius:18px;padding:1.35rem;min-height:190px;margin-bottom:.7rem;box-shadow:0 5px 18px rgba(15,23,42,.035)}.lens-card-icon{font-size:1.35rem}.lens-card-stage{margin-top:.75rem;color:var(--primary);font-size:.7rem;font-weight:800;letter-spacing:.1em}.lens-card-title{color:var(--ink);font-size:1.18rem;font-weight:800;margin:.25rem 0 .45rem}.lens-card-copy{color:var(--muted);font-size:.9rem;line-height:1.55}.lens-principle{background:#F1F5F9;border-radius:14px;padding:1rem;color:#475569;text-align:center;font-size:.88rem;margin-top:1.2rem}
@media(max-width:760px){.block-container{padding-top:3.5rem}.lens-flow{grid-template-columns:repeat(2,1fr)}.lens-hero{padding:2rem 1.4rem}.lens-hero h1{font-size:2.25rem}}

/* PromptLENS Phase 2 */
.lens-page-kicker{color:var(--primary);font-size:.72rem;font-weight:850;letter-spacing:.12em;margin-top:.25rem}
.lens-page-note{background:#F8FAFF;border:1px solid #E0E7FF;border-left:4px solid var(--primary);border-radius:12px;padding:.9rem 1rem;color:#526079;margin:.8rem 0 1.1rem}
.lens-section-label{color:#6366F1;font-size:.68rem;font-weight:850;letter-spacing:.11em;margin-bottom:-.25rem}
div[data-testid="stVerticalBlockBorderWrapper"]{background:#FFFFFF;border:1px solid #E2E8F0 !important;border-radius:18px !important;box-shadow:0 5px 18px rgba(15,23,42,.025);margin-bottom:.85rem}
div[data-testid="stVerticalBlockBorderWrapper"] h3{margin-top:.1rem}
div[data-baseweb="select"]>div, div[data-testid="stTextInput"] input, div[data-testid="stNumberInput"] input, textarea{border-radius:10px !important}
.lens-action-zone{margin-top:1.25rem;background:linear-gradient(135deg,#312E81,#4F46E5);border-radius:18px;padding:1.35rem 1.5rem;color:white;box-shadow:0 10px 26px rgba(79,70,229,.14)}
.lens-action-kicker{font-size:.68rem;font-weight:850;letter-spacing:.12em;opacity:.75}.lens-action-title{font-size:1.15rem;font-weight:800;margin:.3rem 0}.lens-action-copy{font-size:.88rem;line-height:1.55;opacity:.84;max-width:780px}
.lens-result-label{margin-top:2rem;color:var(--primary);font-size:.7rem;font-weight:850;letter-spacing:.12em}.lens-judgement-note{background:#F8FAFC;border:1px solid var(--border);border-radius:12px;padding:.85rem 1rem;color:#526079;font-size:.88rem}

/* LangMRI Phase 3 */
.mri-kicker{color:var(--primary);font-size:.72rem;font-weight:850;letter-spacing:.12em;margin-top:.25rem}
.mri-intro{background:linear-gradient(135deg,#FFFFFF,#F8FAFF);border:1px solid #E0E7FF;border-radius:18px;padding:1.15rem 1.25rem;margin:.7rem 0 1.25rem}
.mri-intro-title{color:var(--ink);font-weight:800;font-size:1rem;margin-bottom:.25rem}
.mri-intro-copy{color:#526079;font-size:.88rem;line-height:1.55}
.mri-section-label{color:#6366F1;font-size:.68rem;font-weight:850;letter-spacing:.11em;margin-bottom:.15rem}
.mri-spec{background:#FFFFFF;border:1px solid var(--border);border-radius:18px;padding:1.15rem 1.25rem;margin:.6rem 0 1rem;box-shadow:0 5px 18px rgba(15,23,42,.025)}
.mri-meta{display:flex;flex-wrap:wrap;gap:.45rem;margin-top:.8rem}
.mri-chip{background:#F8FAFC;border:1px solid #E2E8F0;border-radius:999px;padding:.35rem .65rem;color:#475569;font-size:.78rem}
.mri-run-zone{background:linear-gradient(135deg,#172033,#312E81);border-radius:18px;padding:1.2rem 1.4rem;margin:1.15rem 0 .55rem;color:white}
.mri-run-zone strong{color:white}.mri-run-zone span{opacity:.82;font-size:.88rem}
.mri-report-kicker{color:var(--primary);font-size:.7rem;font-weight:850;letter-spacing:.12em;margin-top:2rem}
.mri-status-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;margin:.7rem 0 1rem}
.mri-status{background:#fff;border:1px solid var(--border);border-radius:16px;padding:1rem 1.05rem}
.mri-status.supported{border-left:4px solid #16A34A}.mri-status.review{border-left:4px solid #D97706}.mri-status.mismatch{border-left:4px solid #DC2626}.mri-status.other{border-left:4px solid #94A3B8}
.mri-status-lens{color:#64748B;font-size:.72rem;font-weight:800;letter-spacing:.08em}.mri-status-value{color:var(--ink);font-size:1.05rem;font-weight:850;margin-top:.2rem}
.mri-status.supported .mri-status-value{color:#15803D}.mri-status.review .mri-status-value{color:#B45309}.mri-status.mismatch .mri-status-value{color:#B91C1C}
.mri-evidence-note{background:#F8FAFC;border:1px solid var(--border);border-radius:12px;padding:.8rem 1rem;color:#526079;font-size:.85rem;margin-bottom:.9rem}
@media(max-width:760px){.mri-status-grid{grid-template-columns:1fr}}


/* LENSFix Phase 4 */
.fix-kicker{color:var(--primary);font-size:.72rem;font-weight:850;letter-spacing:.12em;margin-top:.25rem}
.fix-intro{background:linear-gradient(135deg,#FFFFFF,#F5F3FF);border:1px solid #E0E7FF;border-radius:18px;padding:1.15rem 1.25rem;margin:.7rem 0 1.2rem}
.fix-intro-title{color:var(--ink);font-weight:850;font-size:1rem;margin-bottom:.25rem}
.fix-intro-copy{color:#526079;font-size:.88rem;line-height:1.55}
.fix-principle{background:#F8FAFC;border:1px solid var(--border);border-left:4px solid #4F46E5;border-radius:12px;padding:.85rem 1rem;color:#526079;font-size:.87rem;margin:.65rem 0 1.1rem}
.fix-section-label{color:#6366F1;font-size:.68rem;font-weight:850;letter-spacing:.11em;margin-bottom:.2rem}
.fix-review-head{background:#fff;border:1px solid var(--border);border-radius:16px;padding:1rem 1.1rem;margin:.65rem 0 .8rem}
.fix-review-title{color:var(--ink);font-size:1.05rem;font-weight:850}.fix-review-meta{color:#64748B;font-size:.8rem;margin-top:.2rem}
.fix-brief{background:linear-gradient(135deg,#172033,#312E81);border-radius:18px;padding:1.25rem 1.4rem;margin:1.2rem 0 .7rem;color:#fff}
.fix-brief-title{font-size:1.05rem;font-weight:850;color:#fff}.fix-brief-copy{font-size:.86rem;opacity:.82;margin-top:.25rem}
.fix-ready{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:14px;padding:.9rem 1rem;color:#166534;margin:.9rem 0}

/* LENSFix readability patch — keep headings visible on light cards */
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6{
    color:#172033 !important;
}
.stApp h1 span, .stApp h2 span, .stApp h3 span,
.stApp h4 span, .stApp h5 span, .stApp h6 span,
.stApp h1 a, .stApp h2 a, .stApp h3 a,
.stApp h4 a, .stApp h5 a, .stApp h6 a{
    color:#172033 !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] h1,
div[data-testid="stVerticalBlockBorderWrapper"] h2,
div[data-testid="stVerticalBlockBorderWrapper"] h3,
div[data-testid="stVerticalBlockBorderWrapper"] h4,
div[data-testid="stVerticalBlockBorderWrapper"] h5,
div[data-testid="stVerticalBlockBorderWrapper"] h6{
    color:#172033 !important;
}

/* LENSRevise — cool lavender workspace */
.stApp:has(.lensrevise-page-marker){
    background:
        radial-gradient(circle at 12% 8%, rgba(196,181,253,.34), transparent 28%),
        radial-gradient(circle at 88% 18%, rgba(165,180,252,.30), transparent 30%),
        linear-gradient(145deg,#F8F7FF 0%,#F4F7FF 48%,#EEF2FF 100%);
}
.lensrevise-glow{
    background:linear-gradient(135deg,rgba(255,255,255,.92),rgba(245,243,255,.92));
    border:1px solid #DDD6FE;
    border-radius:20px;
    padding:1.15rem 1.3rem;
    box-shadow:0 12px 32px rgba(79,70,229,.08);
    margin:.7rem 0 1.2rem;
}

</style>""",unsafe_allow_html=True)

def render_brand():
    st.markdown("""<div class="lens-brand"><div class="lens-mark">L</div><div><div class="lens-brand-name">LENSuite ELT</div><div class="lens-brand-sub">Linguistically informed decision support</div></div></div>""",unsafe_allow_html=True)

def render_workflow(active_page):
    mapping={"prompt":0,"langmri":1,"lensfix":2,"lensrevise":3}; active=mapping.get(active_page,-1)
    steps=[("01","✦ DESIGN","PromptLENS"),("02","◉ DIAGNOSE","LangMRI"),("03","◇ DECIDE","LENSFix"),("04","↻ REVISE","LENSRevise")]
    cards=[]
    for i,(num,label,name) in enumerate(steps):
        state="active" if i==active else ("done" if active>i else "")
        cards.append(f'<div class="lens-step {state}"><div class="lens-step-num">{num} · {label}</div><div class="lens-step-name">{name}</div></div>')
    st.markdown('<div class="lens-flow">'+''.join(cards)+'</div>',unsafe_allow_html=True)



# ============================================================



# HOME PAGE



# ============================================================



def home_page():
    render_brand()
    st.markdown("""<div class="lens-hero"><div class="lens-kicker">AI-ASSISTED ELT · TEACHER-CONTROLLED</div><h1>Design with intention.<br>Decide with evidence.</h1><p>LENSuite helps English language teachers design informed prompts, examine generated materials, make professional revision decisions, and translate those decisions into controlled revisions.</p></div>""",unsafe_allow_html=True)
    render_workflow("home")
    st.write("### One workflow. Four focused lenses.")
    st.caption("Move from design intention to diagnostic evidence and teacher-approved revision without surrendering professional judgement.")
    cols=st.columns(4)
    cards=[
      (cols[0],"✦","01 · DESIGN","PromptLENS","Build linguistically, pedagogically and contextually informed prompts.","Open PromptLENS","prompt"),
      (cols[1],"◉","02 · DIAGNOSE","LangMRI","Examine observable linguistic characteristics and requested material features.","Open LangMRI","langmri"),
      (cols[2],"◇","03 · DECIDE","LENSFix","Review diagnostic findings and record teacher-controlled revision decisions.","Open LENSFix","lensfix"),
      (cols[3],"↻","04 · REVISE","LENSRevise","Package approved decisions into a controlled revision prompt for GenAI.","Open LENSRevise","lensrevise") ]
    for col,icon,stage,title,copy,button,page in cards:
      with col:
        st.markdown(f'<div class="lens-card"><div class="lens-card-icon">{icon}</div><div class="lens-card-stage">{stage}</div><div class="lens-card-title">{title}</div><div class="lens-card-copy">{copy}</div></div>',unsafe_allow_html=True)
        if st.button(button,use_container_width=True,key=f"home_{page}"):
          st.session_state.page=page; st.rerun()
    st.markdown("""<div class="lens-principle"><strong>Teacher-in-the-loop by design.</strong> LENSuite provides diagnostic and revision support; the teacher remains the final decision-maker.</div>""",unsafe_allow_html=True)



def build_lexical_evidence_profile(spec):
    """Build a serialisable lexical evidence profile for the diagnostic package.

    The profile records contextual evidence only. It does not assign word-level
    CEFR labels or convert corpus frequency into a difficulty judgement.
    """
    school_level = spec.get("school_level") or "Not specified"
    cefr = spec.get("cefr") or "Not specified"
    vocab_profile = spec.get("vocabulary") or "Not specified"
    vocab_focus = spec.get("vocab_target") or "Not specified"

    if school_level == "Tertiary":
        layers = [
            {"label": "Course / programme context", "value": spec.get("curriculum_reference") or "Teacher/course-defined tertiary programme"},
            {"label": "Programme level", "value": spec.get("programme_level") or "Not specified"},
            {"label": "Language purpose", "value": spec.get("language_purpose") or "Not specified"},
            {"label": "Discipline / programme", "value": spec.get("discipline") or "Not specified"},
            {"label": "Course learning outcome", "value": spec.get("course_outcome") or "Not specified"},
            {"label": "CEFR lexical expectation", "value": cefr},
            {"label": "Vocabulary profile", "value": vocab_profile},
            {"label": "Vocabulary / topic focus", "value": vocab_focus},
            {"label": "Corpus evidence", "value": "SUBTLEX-US frequency is used as a review signal, not a CEFR classifier"},
        ]
        context_type = "tertiary"
    else:
        textbook = spec.get("textbook_reference") or "Not specified"
        unit = spec.get("textbook_unit")
        if unit:
            textbook = f"{textbook} · {unit}"
        layers = [
            {"label": "Curriculum context", "value": spec.get("curriculum_reference") or spec.get("alignment_pathway") or "Not specified"},
            {"label": "Education stage", "value": spec.get("education_stage") or school_level},
            {"label": "Textbook / unit evidence", "value": textbook},
            {"label": "CEFR lexical expectation", "value": cefr},
            {"label": "Vocabulary profile", "value": vocab_profile},
            {"label": "Vocabulary / topic focus", "value": vocab_focus},
            {"label": "Corpus evidence", "value": "SUBTLEX-US frequency is used as a review signal, not a CEFR classifier"},
        ]
        context_type = "school"

    return {
        "context_type": context_type,
        "evidence_layers": layers,
        "interpretation_rule": "frequency ≠ CEFR level ≠ difficulty",
    }


def render_lexical_evidence_profile(spec):
    """Render the contextual evidence LangMRI/LENSFix should consider for lexical review.

    This is an interpretation aid only; it does not assign word-level CEFR labels.
    """
    school_level = spec.get("school_level") or "Not specified"
    cefr = spec.get("cefr") or "Not specified"
    vocab_profile = spec.get("vocabulary") or "Not specified"
    vocab_focus = spec.get("vocab_target") or "Not specified"

    st.markdown("**Lexical Evidence Profile**")
    st.caption(
        "Use these evidence layers together. No single layer automatically determines whether a word is suitable."
    )

    if school_level == "Tertiary":
        rows = [
            ("Course / programme context", spec.get("curriculum_reference") or "Teacher/course-defined tertiary programme"),
            ("Programme level", spec.get("programme_level") or "Not specified"),
            ("Language purpose", spec.get("language_purpose") or "Not specified"),
            ("Discipline / programme", spec.get("discipline") or "Not specified"),
            ("Course learning outcome", spec.get("course_outcome") or "Not specified"),
            ("CEFR lexical expectation", cefr),
            ("Vocabulary profile", vocab_profile),
            ("Vocabulary / topic focus", vocab_focus),
            ("Corpus evidence", "SUBTLEX-US frequency is used as a review signal, not a CEFR classifier"),
        ]
    else:
        textbook = spec.get("textbook_reference") or "Not specified"
        unit = spec.get("textbook_unit")
        if unit:
            textbook = f"{textbook} · {unit}"
        rows = [
            ("Curriculum context", spec.get("curriculum_reference") or spec.get("alignment_pathway") or "Not specified"),
            ("Education stage", spec.get("education_stage") or school_level),
            ("Textbook / unit evidence", textbook),
            ("CEFR lexical expectation", cefr),
            ("Vocabulary profile", vocab_profile),
            ("Vocabulary / topic focus", vocab_focus),
            ("Corpus evidence", "SUBTLEX-US frequency is used as a review signal, not a CEFR classifier"),
        ]

    for label, value in rows:
        st.write(f"**{label}:** {value}")

    st.info(
        "Interpretation rule: frequency ≠ CEFR level ≠ difficulty. Curriculum, textbook/course and corpus evidence support teacher judgement; they do not replace it."
    )


def build_clean_prompt(spec):
    """Build a compact, model-agnostic prompt while preserving teacher specifications."""
    def shown(value, fallback="Not specified"):
        if value is None or value == "" or value == []:
            return fallback
        if isinstance(value, list):
            return ", ".join(str(v) for v in value) if value else fallback
        return str(value)

    learner = [
        f"- Level: {shown(spec.get('school_level'))}",
        f"- CEFR target: {shown(spec.get('cefr'))}",
        f"- Age: {shown(spec.get('age'))}",
    ]

    alignment = [
        f"- Pathway: {shown(spec.get('alignment_pathway'))}",
        f"- Stage: {shown(spec.get('education_stage'))}",
        f"- Curriculum/course reference: {shown(spec.get('curriculum_reference'))}",
    ]
    optional_alignment = [
        ("Textbook/coursebook", spec.get("textbook_reference")),
        ("Unit/topic", spec.get("textbook_unit")),
        ("Programme level", spec.get("programme_level")),
        ("Language purpose", spec.get("language_purpose")),
        ("Discipline/programme", spec.get("discipline")),
        ("Course learning outcome", spec.get("course_outcome")),
    ]
    for label, value in optional_alignment:
        if value:
            alignment.append(f"- {label}: {value}")

    material = [
        f"- Primary skill: {shown(spec.get('skill'))}",
        f"- Resource type: {shown(spec.get('resource_type'))}",
        f"- Topic/theme: {shown(spec.get('topic'), 'Teacher-selected or contextually appropriate')}",
        f"- Length: {shown(spec.get('material_length'))}",
        f"- Tasks/questions: {shown(spec.get('num_tasks'))}",
        f"- Genre: {shown(spec.get('genre'))}",
        f"- Register: {shown(spec.get('register'))}",
        f"- Communicative function: {shown(spec.get('communicative_function'))}",
    ]

    language = [
        f"- Vocabulary profile: {shown(spec.get('vocabulary'))}",
        f"- Vocabulary/topic focus: {shown(spec.get('vocab_target'))}",
        f"- Target grammar: {shown(spec.get('grammar'))}",
    ]

    pedagogy = [
        f"- Learning objective: {shown(spec.get('objective'))}",
        f"- Teaching approach: {shown(spec.get('approach'))}",
        f"- Lesson duration: {shown(spec.get('duration'))} minutes",
        f"- Classroom/context requirements: {shown(spec.get('context'))}",
        f"- Constraints: {shown(spec.get('constraints'))}",
    ]

    output = [
        f"- Learner scaffolding: {shown(spec.get('scaffolding'), 'None requested')}",
        f"- Teacher resources: {shown(spec.get('output_features'), 'None requested')}",
    ]

    sections = [
        "ROLE & TASK\nYou are an English language materials designer. Create the requested ELT resource from the teacher specification below.",
        "LEARNER PROFILE\n" + "\n".join(learner),
        "ALIGNMENT CONTEXT\n" + "\n".join(alignment),
        "MATERIAL\n" + "\n".join(material),
        "LINGUISTIC REQUIREMENTS\n" + "\n".join(language),
        "PEDAGOGICAL & CONTEXTUAL REQUIREMENTS\n" + "\n".join(pedagogy),
        "OUTPUT REQUIREMENTS\n" + "\n".join(output),
        (
            "FINAL INSTRUCTION\n"
            "Follow the teacher specification closely. Keep the material appropriate for the stated learners, purpose and context. "
            "Treat curriculum, textbook and course information as contextual alignment evidence, not automatic word-level CEFR certification. "
            "Do not infer an individual word's CEFR level solely from textbook presence or corpus frequency. "
            "Do not add unnecessary components that the teacher did not request."
        ),
    ]
    return "\n\n".join(sections)

# ============================================================



# PROMPTLENS PAGE



# ============================================================



def promptlens_page():
    render_brand()
    render_workflow("prompt")

    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.markdown('<div class="lens-page-kicker">01 · DESIGN</div>', unsafe_allow_html=True)
        st.title("PromptLENS")
        st.write(
            "Translate your teaching intention into a linguistically, "
            "pedagogically and contextually informed generation prompt."
        )
    with top_right:
        st.write("")
        if st.button("← Home", use_container_width=True, key="prompt_home"):
            st.session_state.page = "home"
            st.rerun()

    st.markdown(
        '<div class="lens-page-note"><strong>Build the specification first.</strong> '
        'PromptLENS packages your choices for GenAI; it does not replace teacher judgement.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    # 1. LEARNER PROFILE
    with st.container(border=True):
        st.markdown('<div class="lens-section-label">01 · LEARNER</div>', unsafe_allow_html=True)
        st.subheader("Learner Profile")
        st.caption("Define who the material is for and the intended proficiency target.")
        col1, col2, col3 = st.columns(3)
        with col1:
            school_level = st.selectbox(
                "School level",
                ["Primary", "Lower Secondary", "Upper Secondary", "Tertiary"]
            )
        with col2:
            cefr = st.selectbox("Target CEFR level", ["A1", "A2", "B1", "B2", "C1"])
        with col3:
            age = st.text_input("Learner age", placeholder="e.g. 14")

    # 1B. ALIGNMENT PROFILE
    with st.container(border=True):
        st.markdown('<div class="lens-section-label">ALIGNMENT</div>', unsafe_allow_html=True)
        st.subheader("Alignment Profile")
        st.caption(
            "Choose the reference context that should inform the material. "
            "Alignment evidence supports teacher judgement; it does not automatically certify a resource."
        )

        if school_level != "Tertiary":
            alignment_pathway = st.selectbox(
                "Alignment pathway",
                ["Malaysian curriculum (KSSR / KSSM)", "Teacher-defined / other curriculum"],
                key="alignment_pathway_school"
            )
            if school_level == "Primary":
                education_stage = st.selectbox(
                    "Year", ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6"],
                    key="school_year_primary"
                )
            elif school_level == "Lower Secondary":
                education_stage = st.selectbox(
                    "Form", ["Form 1", "Form 2", "Form 3"], key="school_form_lower"
                )
            else:
                education_stage = st.selectbox(
                    "Form", ["Form 4", "Form 5"], key="school_form_upper"
                )

            if alignment_pathway == "Malaysian curriculum (KSSR / KSSM)":
                curriculum_reference = (
                    f"KSSR English {education_stage}" if school_level == "Primary"
                    else f"KSSM English {education_stage}"
                )
                st.info(
                    f"Reference context: {curriculum_reference}. "
                    "Use DSKP / Scheme of Work and textbook evidence as contextual references where verified."
                )
                textbook_reference = st.text_input(
                    "Textbook reference (optional)",
                    value="English Download" if education_stage == "Form 5" else "",
                    placeholder="Enter the textbook used by the class",
                    help="Textbook evidence indicates learner exposure/context; it is not treated as a CEFR word-level label."
                )
                textbook_unit = st.text_input(
                    "Textbook unit / topic (optional)",
                    placeholder="e.g. Unit 3 or the current textbook topic"
                )
            else:
                curriculum_reference = st.text_input(
                    "Curriculum / syllabus reference",
                    placeholder="e.g. school syllabus, international curriculum, teacher-defined programme"
                )
                textbook_reference = st.text_input(
                    "Textbook / coursebook reference (optional)",
                    placeholder="Book title"
                )
                textbook_unit = st.text_input(
                    "Unit / topic (optional)", placeholder="Unit or topic"
                )

            programme_level = ""
            language_purpose = ""
            discipline = ""
            course_outcome = ""

        else:
            alignment_pathway = "Tertiary course / programme alignment"
            education_stage = "Tertiary"
            curriculum_reference = "Teacher/course-defined tertiary programme"
            textbook_reference = ""
            textbook_unit = ""

            col_a, col_b = st.columns(2)
            with col_a:
                programme_level = st.selectbox(
                    "Programme level",
                    ["Foundation / Pre-university", "Diploma", "Undergraduate", "Postgraduate", "Other"],
                    key="tertiary_programme_level"
                )
                language_purpose = st.selectbox(
                    "Language purpose",
                    ["General English", "English for Academic Purposes (EAP)",
                     "English for Specific Purposes (ESP)", "Professional communication",
                     "Teacher-defined"],
                    key="tertiary_language_purpose"
                )
            with col_b:
                discipline = st.text_input(
                    "Programme / discipline",
                    placeholder="e.g. Engineering, Business, TESOL, Applied Linguistics"
                )
            course_outcome = st.text_area(
                "Course learning outcome / syllabus outcome (optional)",
                placeholder="Paste the relevant CLO, course outcome or programme requirement here."
            )
            st.caption(
                "For tertiary materials, the course/programme outcome is the primary local alignment reference. "
                "CEFR can remain a proficiency reference rather than being treated as the curriculum itself."
            )

    # 2. LANGUAGE TARGET
    with st.container(border=True):
        st.markdown('<div class="lens-section-label">02 · LANGUAGE</div>', unsafe_allow_html=True)
        st.subheader("Language Target")
        st.caption("Specify the primary skill and the language features you want the material to foreground.")
        col1, col2 = st.columns(2)
        with col1:
            skill = st.selectbox(
                "Primary language skill",
                ["Reading", "Writing", "Speaking", "Listening"]
            )
            grammar = st.text_input(
                "Target grammar",
                placeholder="e.g. Simple past tense"
            )
        with col2:
            vocabulary = st.selectbox(
                "Vocabulary profile",
                [
                    "High-frequency vocabulary",
                    "Topic-specific vocabulary",
                    "Academic vocabulary",
                    "Teacher-defined vocabulary"
                ]
            )
            vocab_target = st.text_input(
                "Specific vocabulary or topic",
                placeholder="e.g. travel and holidays"
            )

        use_alignment_for_lexis = st.checkbox(
            "Use curriculum / course context when interpreting lexical findings",
            value=True,
            help=(
                "Recommended. LangMRI will present textbook, curriculum or tertiary course context "
                "alongside corpus-frequency evidence. This does not automatically mark a word as suitable."
            )
        )
        st.caption(
            "Lexical evidence model: alignment context → CEFR lexical expectation → teacher-selected focus → "
            "SUBTLEX-US frequency → teacher judgement."
        )

    # 3. DISCOURSE & COMMUNICATION
    with st.container(border=True):
        st.markdown('<div class="lens-section-label">03 · DISCOURSE</div>', unsafe_allow_html=True)
        st.subheader("Discourse & Communication")
        st.caption("Shape how the material communicates: its genre, register and communicative purpose.")
        col1, col2 = st.columns(2)
        with col1:
            genre = st.selectbox(
                "Genre",
                [
                    "Narrative", "Descriptive", "Informative", "Argumentative",
                    "Dialogue", "Email", "Article", "Other"
                ]
            )
        with col2:
            register = st.selectbox(
                "Register",
                ["Informal", "Neutral", "Semi-formal", "Formal"]
            )
        communicative_function = st.text_input(
            "Communicative function",
            placeholder="e.g. describing past experiences"
        )

    # 4. MATERIAL DESIGN
    with st.container(border=True):
        st.markdown('<div class="lens-section-label">04 · MATERIAL</div>', unsafe_allow_html=True)
        st.subheader("Material Design")
        st.caption("Define the resource format, theme, length and support that learners and teachers should receive.")
        col1, col2 = st.columns(2)
        with col1:
            resource_type = st.selectbox(
                "Resource type",
                [
                    "Reading passage", "Worksheet", "Speaking activity", "Writing task",
                    "Listening activity", "Grammar exercise", "Vocabulary activity",
                    "Quiz", "Lesson activity", "Other"
                ]
            )
            topic = st.text_input(
                "Topic or theme",
                placeholder="e.g. Environmental awareness"
            )
        with col2:
            material_length = st.selectbox("Material length", ["Short", "Medium", "Long"])
            num_tasks = st.number_input(
                "Number of tasks/questions",
                min_value=1,
                max_value=20,
                value=5
            )
        st.markdown("**Learner scaffolding**")
        scaffolding = st.multiselect(
            "Select scaffolding features",
            [
                "Clear instructions", "Example / model", "Vocabulary support",
                "Sentence starters", "Guiding questions", "Extension task"
            ],
            default=["Clear instructions"]
        )
        output_features = st.multiselect(
            "Additional teacher resources",
            ["Answer key", "Teacher notes"]
        )

    # 5. PEDAGOGICAL REQUIREMENTS
    with st.container(border=True):
        st.markdown('<div class="lens-section-label">05 · PEDAGOGY</div>', unsafe_allow_html=True)
        st.subheader("Pedagogical Requirements")
        st.caption("Anchor the generated resource to a learning objective, teaching approach and realistic lesson duration.")
        objective = st.text_area(
            "Learning objective",
            placeholder=(
                "e.g. Students will be able to identify specific information "
                "in a narrative text."
            )
        )
        col1, col2 = st.columns(2)
        with col1:
            approach = st.selectbox(
                "Teaching approach",
                [
                    "Communicative Language Teaching",
                    "Task-Based Language Teaching",
                    "Text-Based Approach",
                    "Not specified"
                ]
            )
        with col2:
            duration = st.number_input(
                "Lesson duration (minutes)",
                min_value=10,
                max_value=180,
                value=60,
                step=5
            )

    # 6. CLASSROOM CONTEXT
    with st.container(border=True):
        st.markdown('<div class="lens-section-label">06 · CONTEXT</div>', unsafe_allow_html=True)
        st.subheader("Classroom Context")
        st.caption("Add local, cultural and practical conditions that should shape the material.")
        context = st.text_area(
            "Contextual requirements",
            placeholder=(
                "e.g. Malaysian Form 2 classroom; use culturally familiar "
                "situations where appropriate."
            )
        )
        constraints = st.text_area(
            "Classroom constraints",
            placeholder="e.g. mixed proficiency, limited technology, 40 students"
        )

    # BUILD ACTION
    st.markdown(
        '<div class="lens-action-zone"><div class="lens-action-kicker">SPECIFICATION READY?</div>'
        '<div class="lens-action-title">Turn your teaching decisions into a generation prompt.</div>'
        '<div class="lens-action-copy">PromptLENS will preserve the specification above and structure it for use with your preferred generative AI tool.</div></div>',
        unsafe_allow_html=True
    )

    if st.button(
        "✦ BUILD MY PROMPT",
        type="primary",
        use_container_width=True,
        key="build_prompt_phase2"
    ):
        st.session_state["prompt_specification"] = {
            "school_level": school_level,
            "cefr": cefr,
            "age": age,
            "skill": skill,
            "resource_type": resource_type,
            "topic": topic,
            "material_length": material_length,
            "num_tasks": num_tasks,
            "scaffolding": scaffolding,
            "output_features": output_features,
            "grammar": grammar,
            "vocabulary": vocabulary,
            "vocab_target": vocab_target,
            "genre": genre,
            "register": register,
            "communicative_function": communicative_function,
            "objective": objective,
            "approach": approach,
            "duration": duration,
            "context": context,
            "constraints": constraints,
            "alignment_pathway": alignment_pathway,
            "education_stage": education_stage,
            "curriculum_reference": curriculum_reference,
            "textbook_reference": textbook_reference,
            "textbook_unit": textbook_unit,
            "programme_level": programme_level,
            "language_purpose": language_purpose,
            "discipline": discipline,
            "course_outcome": course_outcome,
            "use_alignment_for_lexis": use_alignment_for_lexis
        }

        # Phase B: compact, model-agnostic PromptLENS output.
        # All teacher selections remain available through the saved specification.
        prompt = build_clean_prompt(st.session_state["prompt_specification"])
        st.session_state["generated_prompt"] = prompt

    # GENERATED RESULT
    if "generated_prompt" in st.session_state:
        prompt = st.session_state["generated_prompt"]
        st.markdown('<div class="lens-result-label">PROMPTLENS OUTPUT</div>', unsafe_allow_html=True)
        st.subheader("Your generation prompt is ready")
        st.caption(
            "Use this prompt with your preferred GenAI tool, review the generated material, "
            "then continue to LangMRI for diagnostic examination."
        )
        st.text_area(
            "Generated prompt",
            value=prompt,
            height=430,
            key="generated_prompt_display"
        )
        st.markdown(
            '<div class="lens-judgement-note"><strong>Teacher judgement remains essential.</strong> '
            'PromptLENS structures your specification; it does not certify the suitability of the generated material.</div>',
            unsafe_allow_html=True
        )

        st.markdown("#### Use with your preferred GenAI")
        st.caption("Open a tool, then copy and paste the PromptLENS output above. LENSuite remains model-agnostic and does not send your prompt automatically.")
        ai1, ai2, ai3, ai4 = st.columns(4)
        with ai1:
            st.link_button("Open ChatGPT ↗", "https://chatgpt.com", use_container_width=True)
        with ai2:
            st.link_button("Open Claude ↗", "https://claude.ai", use_container_width=True)
        with ai3:
            st.link_button("Open Gemini ↗", "https://gemini.google.com", use_container_width=True)
        with ai4:
            st.link_button("Open Copilot ↗", "https://copilot.com", use_container_width=True)

        st.write("")
        if st.button(
            "Continue to LangMRI  →",
            type="primary",
            use_container_width=True,
            key="continue_to_langmri"
        ):
            st.session_state.page = "langmri"
            st.rerun()


# ============================================================
# LANGMRI PAGE
# ============================================================

def langmri_page():

    render_brand()
    render_workflow("langmri")

    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.markdown('<div class="mri-kicker">02 · DIAGNOSE</div>', unsafe_allow_html=True)
        st.title("LangMRI")
    with top_right:
        st.write("")
        if st.button("← Home", use_container_width=True, key="mri_home"):
            st.session_state.page = "home"
            st.rerun()



    st.write(



        "Examine observable linguistic characteristics "



        "of AI-generated English teaching materials."



    )



    st.markdown(
        '<div class="mri-intro"><div class="mri-intro-title">Diagnostic evidence, not automatic certification.</div>'
        '<div class="mri-intro-copy">LangMRI examines observable linguistic characteristics within the analysis scope selected by the teacher. '
        'Results support professional judgement and do not constitute formal CEFR certification.</div></div>',
        unsafe_allow_html=True
    )



    st.divider()



    # ========================================================



    # TARGET PROFILE



    # ========================================================



    st.markdown('<div class="mri-section-label">INTENDED SPECIFICATION</div>', unsafe_allow_html=True)
    st.subheader("Reference Profile")



    saved_spec = st.session_state.get(



        "prompt_specification"



    )



    if saved_spec:



        st.success(



            "PromptLENS specification detected."



        )



        col1, col2, col3 = st.columns(3)



        col1.metric(



            "CEFR",



            saved_spec["cefr"]



        )



        col2.metric(



            "Primary Skill",



            saved_spec["skill"]



        )



        col3.metric(



            "Resource",



            saved_spec["resource_type"]



        )



        st.write(



            f'**Topic:** {saved_spec["topic"] or "Not specified"}'



        )



        st.write(



            f'**Target grammar:** '



            f'{saved_spec["grammar"] or "Not specified"}'



        )



        st.write(



            f'**Vocabulary profile:** '



            f'{saved_spec["vocabulary"]}'



        )



        st.write(



            f'**Vocabulary/topic focus:** '



            f'{saved_spec["vocab_target"] or "Not specified"}'



        )



        st.write(



            f'**Genre:** {saved_spec["genre"]}'



        )



        st.write(



            f'**Register:** {saved_spec["register"]}'



        )

        st.write(
            f'**Alignment:** {saved_spec.get("curriculum_reference") or saved_spec.get("alignment_pathway") or "Not specified"}'
        )
        if saved_spec.get("textbook_reference"):
            unit_label = f' · {saved_spec.get("textbook_unit")}' if saved_spec.get("textbook_unit") else ""
            st.write(f'**Textbook evidence:** {saved_spec.get("textbook_reference")}{unit_label}')
        if saved_spec.get("programme_level"):
            st.write(
                f'**Tertiary context:** {saved_spec.get("programme_level")} · '
                f'{saved_spec.get("language_purpose") or "Purpose not specified"} · '
                f'{saved_spec.get("discipline") or "Discipline not specified"}'
            )



        if saved_spec.get("use_alignment_for_lexis", True):
            st.markdown("#### Lexical Evidence Profile")
            render_lexical_evidence_profile(saved_spec)

        target_cefr = saved_spec["cefr"]



    else:



        st.warning(



            "No PromptLENS specification was found. "



            "You can still run a standalone analysis."



        )



        target_cefr = st.selectbox(



            "Intended CEFR level",



            [



                "A1",



                "A2",



                "B1",



                "B2",



                "C1"



            ],



            key="langmri_cefr"



        )



    # ========================================================



    # ANALYSIS SCOPE



    # ========================================================



    st.markdown('<div class="mri-section-label">ANALYSIS INPUT</div>', unsafe_allow_html=True)
    st.subheader("Analysis Scope")



    analysis_scope = st.selectbox(



        "What are you analysing?",



        [



            "Learner-facing text",



            "Task / instructions",



            "Complete learner resource",



            "Teacher-facing material",



            "Custom text"



        ]



    )



    scope_explanations = {



        "Learner-facing text":



            "Analyse language that learners are expected to "



            "read, listen to or otherwise process as input.",



        "Task / instructions":



            "Analyse the language used to explain what learners "



            "are expected to do.",



        "Complete learner resource":



            "Analyse the complete learner-facing resource, "



            "including input, tasks, questions and scaffolding.",



        "Teacher-facing material":



            "Analyse notes, guidance or other language intended "



            "primarily for teachers.",



        "Custom text":



            "Analyse a teacher-selected extract or other "



            "specific text."



    }



    st.caption(



        scope_explanations[analysis_scope]



    )



    # ========================================================



    # MATERIAL INPUT



    # ========================================================



    st.subheader("Material to Analyse")



    material_text = st.text_area(



        "Paste the AI-generated material here",



        height=300,



        placeholder=(



            "Paste a reading passage, worksheet text, "



            "dialogue or other generated ELT material..."



        )



    )



    # ========================================================



    # ANALYSIS



    # ========================================================



    if st.button(



        "◉ RUN LINGUISTIC MRI",



        type="primary",



        use_container_width=True



    ):



        if not material_text.strip():



            st.warning(



                "Please paste some material before "



                "running the analysis."



            )



        else:



            results = analyse_text(material_text)



            lexical_results = analyse_lexical_frequency(



                material_text



            )



            grammar_flag = None



            discourse_flag = None



            pedagogical_flag = None



            lexical_flag = None



            if saved_spec:



                grammar_flag = evaluate_grammar_target(



                    saved_spec.get("grammar", ""),



                    results["past_form_count"]



                )



                discourse_flag = evaluate_discourse(



                    saved_spec.get("genre", ""),



                    results["sequencing_marker_count"]



                )



                pedagogical_flag = evaluate_requested_components(



                    saved_spec.get("output_features", []),



                    results["answer_key_detected"],



                    results["teacher_notes_detected"]



                )



                lexical_flag = evaluate_lexical_frequency(



                    lexical_results["analysed_items"],



                    vocabulary_profile=saved_spec.get("vocabulary", ""),



                    vocabulary_focus=saved_spec.get("vocab_target", ""),



                    material_topic=saved_spec.get("topic", "")



                )



                # Keep corpus-frequency analysis descriptive.
                # Low frequency alone is not strong enough to create a word-level
                # LENSFix warning (e.g. a familiar topic word may simply be less
                # frequent in the reference corpus).
                lexical_review_items = []



                missing_components = []



                if (



                    "Answer key" in saved_spec.get("output_features", [])



                    and not results["answer_key_detected"]



                ):



                    missing_components.append("Answer key")



                if (



                    "Teacher notes" in saved_spec.get("output_features", [])



                    and not results["teacher_notes_detected"]



                ):



                    missing_components.append("Teacher notes")



                st.session_state["diagnostic_package"] = {



                    "specification": saved_spec,



                    "material_text": material_text,



                    "analysis_scope": analysis_scope,



                    "flags": [



                        lexical_flag,



                        grammar_flag,



                        discourse_flag,



                        pedagogical_flag



                    ],



                    "lexical_review_items": lexical_review_items,

                    "lexical_evidence_profile": build_lexical_evidence_profile(saved_spec),

                    "missing_components": missing_components



                }



            st.success(



                "Initial linguistic scan completed."



            )



            st.caption(



                f'Analysis scope: {analysis_scope} | '



                f'Material received: {results["word_count"]} words | '



                f'{results["character_count"]} characters'



            )



            st.markdown('<div class="mri-report-kicker">LANGMRI · DIAGNOSTIC REPORT</div>', unsafe_allow_html=True)
            st.subheader("Text Profile")



            col1, col2, col3, col4 = st.columns(4)



            col1.metric(



                "Words",



                results["word_count"]



            )



            col2.metric(



                "Sentences",



                results["sentence_count"]



            )



            col3.metric(



                "Avg. sentence length",



                f'{results["average_sentence_length"]} words'



            )



            col4.metric(



                "Longest sentence",



                f'{results["longest_sentence"]} words'



            )



            st.caption(



                "These measurements are descriptive indicators. "



                "They should not be interpreted as fixed CEFR "



                "thresholds or automatic judgements of material quality."



            )



                        # ================================================



            # DIAGNOSTIC SUMMARY



            # ================================================



            if saved_spec:



                st.divider()



                st.subheader("Diagnostic Overview")



                flags = [



                    lexical_flag,



                    grammar_flag,



                    discourse_flag,



                    pedagogical_flag



                ]



                for flag in flags:



                    # Show flag status



                    if flag["status"] == "SUPPORTED":



                        st.success(



                            f'🟢 {flag["lens"]}: '



                            f'{flag["status"]}'



                        )



                    elif flag["status"] == "REVIEW":



                        st.warning(



                            f'🟠 {flag["lens"]}: '



                            f'{flag["status"]}'



                        )



                    elif flag["status"] == "MISMATCH":



                        st.error(



                            f'🔴 {flag["lens"]}: '



                            f'{flag["status"]}'



                        )



                    else:



                        st.info(



                            f'⚪ {flag["lens"]}: '



                            f'{flag["status"]}'



                        )



                    # WHY? explanation



                    with st.expander(



                        f'Why? — {flag["feature"]}'



                    ):



                        st.write(



                            "**Observation**"



                        )



                        st.write(



                            flag["observation"]



                        )



                        st.write(



                            "**Evidence**"



                        )



                        st.write(



                            flag["evidence"]



                        )



                        st.write(



                            "**Interpretation**"



                        )



                        st.write(



                            flag["interpretation"]



                        )



                        # ================================================



            # LEXICAL LENS



            # ================================================



            st.divider()



            st.subheader("Lexical Lens")



            col1, col2 = st.columns(2)



            col1.metric(



                "Unique words",



                results["unique_word_count"]



            )



            col2.metric(



                "Lexical diversity",



                f'{results["lexical_diversity"]}%'



            )



            st.info(



                "Lexical diversity describes variation in the "



                "vocabulary used in this material. It is a "



                "descriptive text indicator and should not be "



                "interpreted as a direct CEFR score."



            )



            st.write(



                "### Corpus Frequency Profile"



            )



            col1, col2 = st.columns(2)



            col1.metric(



                "Matched lexical types",



                lexical_results["matched_count"]



            )



            col2.metric(



                "Not found in corpus",



                lexical_results["unmatched_count"]



            )



            st.caption(



                "Frequency evidence is drawn from the "



                "SUBTLEX-US reference dataset. Corpus "



                "frequency describes how commonly a word "



                "occurs in that reference corpus; it does "



                "not directly determine CEFR level or "



                "pedagogical appropriateness."



            )



            with st.expander("ⓘ Why does LangMRI use SUBTLEX-US?"):
                st.markdown("""
**SUBTLEX-US is used as a lexical-frequency reference — not as a CEFR framework.**

LangMRI needs an empirical reference point for describing how common or uncommon a lexical item is. SUBTLEX-US provides word-frequency estimates derived from a large corpus of American film and television subtitles (approximately 51 million words). Subtitle-based frequency norms provide an empirically grounded account of lexical occurrence and have been validated against human lexical-processing data.

LangMRI uses the **Zipf frequency scale** to make corpus frequencies easier to interpret. Lower Zipf values indicate relatively less frequent words, while higher values indicate more frequent words.

**What this evidence can tell the teacher**
- whether a lexical item is relatively common or less common in the reference corpus;
- which lower-frequency items may deserve closer professional review;
- where vocabulary demands may warrant additional support or contextualisation.

**What it does NOT tell the teacher**
- that a word belongs to a particular CEFR level;
- that a less frequent word is automatically difficult or inappropriate;
- that a material passes or fails a CEFR standard.

Frequency is therefore treated as **diagnostic evidence, not a pedagogical verdict**. The teacher remains responsible for judging vocabulary in relation to learner proficiency, topic, instructional purpose and classroom context.

**Reference basis:** Brysbaert & New (2009), *Behavior Research Methods*; van Heuven et al. (2014), *Quarterly Journal of Experimental Psychology*.
                """)

            if lexical_results["analysed_items"]:



                sorted_items = sorted(



                    lexical_results["analysed_items"],



                    key=lambda item: item["zipf"]



                )



                st.write(



                    "#### 🔎 Vocabulary Frequency"



                )



                st.caption(



                    "This shows how commonly vocabulary in the "



                    "material occurs in the reference corpus. "



                    "Less common does not automatically mean "



                    "difficult or inappropriate."



                )



                table_data = []



                for item in sorted_items:



                    zipf = item["zipf"]



                    if zipf <= 3:



                        frequency_label = "Less common"



                    elif zipf < 4:



                        frequency_label = "Moderately common"



                    elif zipf < 5:



                        frequency_label = "Common"



                    else:



                        frequency_label = "Very common"



                    table_data.append({



                        "Word": item["word"],



                        "Part of speech": item["pos"],



                        "How common?": frequency_label



                    })



                st.dataframe(



                    table_data,



                    use_container_width=True,



                    hide_index=True



                )



    # Keep the LangMRI → LENSFix navigation available after reruns.

    if "diagnostic_package" in st.session_state:



        st.divider()



        st.success(

            "LangMRI analysis complete. "

            "Your diagnostic results are ready for LENSFix."

        )



        if st.button(

            "Continue to LENSFix  →",

            type="primary",

            use_container_width=True,

            key="continue_to_lensfix"

        ):

            st.session_state.page = "lensfix"

            st.rerun()





# ============================================================



# LENSFIX PAGE



# ============================================================




# ============================================================
# PHASE C — LENSFIX INTELLIGENCE HELPERS
# ============================================================
_REPLACEMENT_CANDIDATES = {
 "mitigate":["reduce","lessen","limit"], "detrimental":["harmful","damaging"], "consumption":["use","usage"],
 "utilise":["use"], "utilize":["use"], "commence":["begin","start"], "terminate":["end","stop"],
 "numerous":["many","several"], "sufficient":["enough","adequate"], "subsequent":["later","following"],
 "approximately":["about","around"], "demonstrate":["show","explain"], "facilitate":["help","support","make easier"],
 "obtain":["get","receive"], "purchase":["buy"], "require":["need"], "assist":["help"],
 "indicate":["show","suggest"], "significant":["important","major"], "substantial":["large","considerable"],
 "predominantly":["mainly","mostly"], "consequently":["so","as a result"], "nevertheless":["however","even so"],
 "furthermore":["also","in addition"], "endeavour":["try","attempt"], "acquire":["get","gain","learn"],
 "retain":["keep","remember"], "encounter":["meet","find","experience"], "implement":["use","apply","carry out"],
 "enhance":["improve","strengthen"], "adverse":["harmful","negative"], "viable":["workable","practical"],
 "allocate":["give","set aside","assign"], "conserve":["save","protect"]
}

def get_replacement_candidates(word, spec):
    # Candidate starting points only: never automatic CEFR labels or replacements.
    return _REPLACEMENT_CANDIDATES.get((word or "").strip().lower(), [])

def get_support_recommendations(spec):
    level=(spec.get("school_level") or "").lower(); cefr=(spec.get("cefr") or "").upper(); vocab=(spec.get("vocabulary") or "").lower()
    if level == "tertiary":
        return (["Add a short learner-friendly gloss","Add a contextual example","Highlight it as target vocabulary"]
                if ("academic" in vocab or "topic" in vocab) else ["Add a contextual example","Add a short learner-friendly gloss"])
    if cefr in {"A1","A2"} or level == "primary":
        return ["Add a short learner-friendly gloss","Add a visual cue","Add a contextual example"]
    if cefr in {"B1","B2"}:
        return ["Add a contextual example","Pre-teach the word","Highlight it as target vocabulary"]
    return ["Add a contextual example","Highlight it as target vocabulary","Add a short learner-friendly gloss"]

def lensfix_page():

    render_brand()
    render_workflow("lensfix")

    st.markdown(
        '<div class="fix-intro"><div class="fix-intro-title">A concise review before you use or revise the material.</div>'
        '<div class="fix-intro-copy">LENSFix summarises what LangMRI observed without turning descriptive evidence '
        'into automatic corrections. Use the summary alongside your knowledge of your learners and lesson.</div></div>',
        unsafe_allow_html=True
    )

    top_left, top_right = st.columns([5, 1])
    with top_left:
        st.markdown('<div class="fix-kicker">03 · DECIDE</div>', unsafe_allow_html=True)
        st.title("LENSFix Summary")
    with top_right:
        st.write("")
        if st.button("← Home", use_container_width=True, key="lensfix_home"):
            st.session_state.page = "home"
            st.rerun()

    package = st.session_state.get("diagnostic_package")

    if not package:
        st.warning("No LangMRI diagnostic results are available yet. Run LangMRI first.")
        if st.button("🔬 Go to LangMRI", use_container_width=True, key="lensfix_go_mri"):
            st.session_state.page = "langmri"
            st.rerun()
        return

    spec = package["specification"]
    flags = [f for f in package.get("flags", []) if f]
    missing_components = package.get("missing_components", [])

    with st.expander("ⓘ How is this summary formed?", expanded=False):
        st.markdown(
            """
LENSFix summarises **observable evidence** from LangMRI in relation to the teaching specification you provided.

It considers:
- the intended learner and CEFR target;
- the language, genre, task and resource features requested in PromptLENS;
- curriculum, course or textbook context when provided;
- descriptive linguistic evidence from LangMRI; and
- requested components that were or were not detected.

**Vocabulary is treated cautiously.** Corpus frequency remains background descriptive evidence only. A less-frequent word is not automatically difficult, inappropriate or outside the intended CEFR level. LENSFix therefore does not flag individual words simply because they are uncommon in the reference corpus.

A small amount of appropriately challenging, topic-relevant vocabulary can be useful as a **learning opportunity**, especially when meaning can be inferred from context or supported by the teacher.

The summary is decision support, not certification. **The teacher makes the final judgement.**
            """
        )

    st.markdown(
        '<div class="fix-principle"><strong>Teacher review principle:</strong> '
        'LENSuite describes what it can observe. It does not decide whether the material is good, bad, '
        'easy, difficult or suitable on the teacher’s behalf.</div>',
        unsafe_allow_html=True
    )

    st.subheader("🎯 Teaching Context")
    c1, c2, c3 = st.columns(3)
    c1.metric("CEFR", spec.get("cefr", "Not specified"))
    c2.metric("Primary Skill", spec.get("skill", "Not specified"))
    c3.metric("Resource", spec.get("resource_type", "Not specified"))

    st.caption(
        f'Topic: {spec.get("topic") or "Not specified"}  ·  '
        f'Vocabulary focus: {spec.get("vocab_target") or spec.get("vocabulary") or "Not specified"}'
    )

    st.divider()
    st.subheader("◇ Review Summary")
    st.caption(
        "Use these observations as prompts for professional reflection rather than pass/fail judgements."
    )

    # LANGUAGE / GRAMMAR
    grammar_flag = next(
        (f for f in flags if "grammar" in str(f.get("lens", "")).lower()),
        None
    )
    with st.container(border=True):
        st.markdown("### Language & Grammar")
        if grammar_flag:
            st.write(grammar_flag.get("observation") or grammar_flag.get("interpretation") or
                     "LangMRI recorded descriptive evidence for the requested grammar target.")
        else:
            st.write(
                "Review whether the language patterns in the material support the intended learning objective "
                "and are manageable for your learners."
            )
        st.caption(
            "Consider the target grammar as part of the whole task rather than as an automatic pass/fail feature."
        )

    # VOCABULARY
    with st.container(border=True):
        st.markdown("### Vocabulary & Learning Opportunity")
        st.write(
            "Vocabulary is not flagged word-by-word on frequency alone. Instead, review whether the material is "
            "generally accessible while still giving learners a manageable opportunity to encounter new language."
        )
        st.info(
            "💡 A useful classroom material does not need to contain only familiar words. "
            "One or two appropriately challenging, topic-relevant words can become useful learning opportunities "
            "when learners can understand them through context, explanation or brief support."
        )
        st.caption(
            "Corpus frequency can describe how common a word is in a reference dataset, but it cannot by itself "
            "tell us whether that word is difficult or pedagogically inappropriate for your learners."
        )

    # DISCOURSE / TASK
    discourse_flag = next(
        (f for f in flags if "discourse" in str(f.get("lens", "")).lower()),
        None
    )
    with st.container(border=True):
        st.markdown("### Task, Genre & Communication")
        if discourse_flag:
            st.write(discourse_flag.get("observation") or discourse_flag.get("interpretation") or
                     "LangMRI recorded descriptive evidence related to the requested discourse features.")
        else:
            st.write(
                f'Review whether the material functions as the intended **{spec.get("genre") or "genre"}** '
                f'and supports the intended communicative purpose: '
                f'**{spec.get("communicative_function") or "not specified"}**.'
            )
        st.caption(
            "Genre and communicative appropriateness still require teacher interpretation in relation to the actual task."
        )

    # REQUESTED COMPONENTS
    with st.container(border=True):
        st.markdown("### Requested Resource Features")
        if missing_components:
            missing_text = ", ".join(missing_components)
            st.warning(
                f"LangMRI did not detect the following requested component(s): **{missing_text}**."
            )
            st.write(
                "Check the material yourself before revising, as automatic detection may not capture every format or wording."
            )
        else:
            st.success(
                "No requested answer-key or teacher-note component is currently marked as missing."
            )

    # CONTEXT / ALIGNMENT
    with st.container(border=True):
        st.markdown("### Context & Alignment")
        alignment = (
            spec.get("curriculum_reference")
            or spec.get("alignment_pathway")
            or "Not specified"
        )
        st.write(f"**Reference context:** {alignment}")
        if spec.get("textbook_reference"):
            unit = f' · {spec.get("textbook_unit")}' if spec.get("textbook_unit") else ""
            st.write(f'**Textbook/coursebook:** {spec.get("textbook_reference")}{unit}')
        st.caption(
            "Curriculum, textbook and course information provides context for teacher review; "
            "it is not treated as automatic certification of the generated material."
        )

    st.divider()
    st.subheader("👩‍🏫 Teacher Decision")
    st.write(
        "Based on the summary above and your knowledge of your learners, decide whether the material is ready to use "
        "or whether you want to revise something."
    )

    teacher_decision = st.radio(
        "What would you like to do?",
        [
            "✓ I am happy with the material",
            "✎ I want to revise something"
        ],
        index=None,
        key="lensfix_summary_teacher_decision"
    )

    if teacher_decision == "✓ I am happy with the material":
        st.session_state.pop("lensfix_revision_brief", None)
        st.success(
            "Teacher decision recorded: no revision requested. "
            "You can return to LangMRI or use the material as appropriate for your class."
        )

    elif teacher_decision == "✎ I want to revise something":
        revision_note = st.text_area(
            "What would you like to change?",
            placeholder=(
                "Write your own revision instruction, e.g. "
                "'Keep the content, but add a short vocabulary box for two challenging words.'"
            ),
            height=130,
            key="lensfix_teacher_revision_note"
        )

        if revision_note.strip():
            revision_brief = (
                "Revise the material using ONLY the following teacher-approved change:\n\n"
                f"1. {revision_note.strip()}\n\n"
                "Preserve all other content unless a change is necessary to implement this instruction."
            )
            st.session_state["lensfix_revision_brief"] = revision_brief
            st.markdown(
                '<div class="fix-ready"><strong>Ready for LENSRevise.</strong> '
                'Your own revision decision will be carried forward.</div>',
                unsafe_allow_html=True
            )
        else:
            st.session_state.pop("lensfix_revision_brief", None)
            st.info("Add your revision instruction when you are ready.")

    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("← Back to LangMRI", use_container_width=True, key="lensfix_back_to_mri"):
            st.session_state.page = "langmri"
            st.rerun()
    with nav2:
        if st.session_state.get("lensfix_revision_brief"):
            if st.button(
                "✨ Continue to LENSRevise →",
                type="primary",
                use_container_width=True,
                key="continue_to_lensrevise"
            ):
                st.session_state.page = "lensrevise"
                st.rerun()



# ============================================================



def lensrevise_page():

    st.markdown(
        '<div class="lensrevise-page-marker"></div>',
        unsafe_allow_html=True
    )

    render_brand()
    render_workflow("lensrevise")

    nav_back, nav_home = st.columns([1, 1])

    with nav_back:
        if st.button(
            "← Back to LENSFix",
            use_container_width=True,
            key="lensrevise_back"
        ):
            st.session_state.page = "lensfix"
            st.rerun()

    with nav_home:
        if st.button(
            "⌂ Home",
            use_container_width=True,
            key="lensrevise_home"
        ):
            st.session_state.page = "home"
            st.rerun()

    st.markdown(
        """
        <div class="lensrevise-glow">
            <div class="lens-kicker">04 · REVISE</div>
            <div style="font-size:1.65rem;font-weight:800;color:#172033;
                        margin:.25rem 0 .35rem;">
                ✨ LENSRevise
            </div>
            <div style="color:#526079;line-height:1.6;">
                Convert teacher-approved LENSFix decisions into a
                ready-to-use revision prompt for your preferred
                generative AI tool.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



    st.info(

        "LENSRevise does not make new revision decisions. "

        "It packages only the changes approved by the teacher while "

        "preserving the original teaching specification."

    )



    package = st.session_state.get("diagnostic_package")

    revision_brief = st.session_state.get("lensfix_revision_brief")



    if not package:

        st.warning(

            "No LangMRI diagnostic package is available. "

            "Run LangMRI and LENSFix first."

        )

        if st.button("🔬 Go to LangMRI", use_container_width=True):

            st.session_state.page = "langmri"

            st.rerun()

        return



    if not revision_brief:

        st.warning(

            "No teacher-approved revision brief is available yet. "

            "Complete the required decisions in LENSFix first."

        )

        if st.button("🧭 Go to LENSFix", use_container_width=True):

            st.session_state.page = "lensfix"

            st.rerun()

        return



    spec = package.get("specification", {})

    original_material = package.get("material_text", "")



    st.divider()

    st.subheader("🎯 Revision Context")



    col1, col2, col3 = st.columns(3)

    col1.metric("CEFR", spec.get("cefr", "Not specified"))

    col2.metric("Primary Skill", spec.get("skill", "Not specified"))

    col3.metric("Resource", spec.get("resource_type", "Not specified"))



    st.write(f'**Topic:** {spec.get("topic") or "Not specified"}')

    st.write(f'**Target grammar:** {spec.get("grammar") or "Not specified"}')

    st.write(f'**Genre:** {spec.get("genre") or "Not specified"}')

    st.write(f'**Register:** {spec.get("register") or "Not specified"}')



    st.divider()

    st.subheader("📄 Original Material")



    st.text_area(

        "Material submitted to LangMRI",

        value=original_material,

        height=250,

        key="lensrevise_original_material"

    )



    st.divider()

    st.subheader("🧭 Teacher-Approved Changes")



    st.text_area(

        "LENSFix revision brief",

        value=revision_brief,

        height=180,

        key="lensrevise_revision_brief"

    )



    specification_lines = [

        f'- Learner level: {spec.get("school_level") or "Not specified"}',

        f'- CEFR target: {spec.get("cefr") or "Not specified"}',

        f'- Learner age: {spec.get("age") or "Not specified"}',

        f'- Primary language skill: {spec.get("skill") or "Not specified"}',

        f'- Resource type: {spec.get("resource_type") or "Not specified"}',

        f'- Topic/theme: {spec.get("topic") or "Not specified"}',

        f'- Target grammar: {spec.get("grammar") or "Not specified"}',

        f'- Vocabulary profile: {spec.get("vocabulary") or "Not specified"}',

        f'- Vocabulary/topic focus: {spec.get("vocab_target") or "Not specified"}',

        f'- Genre: {spec.get("genre") or "Not specified"}',

        f'- Register: {spec.get("register") or "Not specified"}',

        f'- Communicative function: {spec.get("communicative_function") or "Not specified"}',

        f'- Learning objective: {spec.get("objective") or "Not specified"}',

        f'- Teaching approach: {spec.get("approach") or "Not specified"}',

        f'- Classroom context: {spec.get("context") or "Not specified"}',

        f'- Classroom constraints: {spec.get("constraints") or "Not specified"}',
        f'- Alignment pathway: {spec.get("alignment_pathway") or "Not specified"}',
        f'- Education stage: {spec.get("education_stage") or "Not specified"}',
        f'- Curriculum/course reference: {spec.get("curriculum_reference") or "Not specified"}',
        f'- Textbook/coursebook reference: {spec.get("textbook_reference") or "Not specified"}',
        f'- Textbook unit/topic: {spec.get("textbook_unit") or "Not specified"}',
        f'- Programme level: {spec.get("programme_level") or "Not specified"}',
        f'- Language purpose: {spec.get("language_purpose") or "Not specified"}',
        f'- Discipline/programme: {spec.get("discipline") or "Not specified"}',
        f'- Course learning outcome: {spec.get("course_outcome") or "Not specified"}'
    ]



    revision_prompt = "\n".join([

        "Revise the English language teaching material below.",

        "",

        "IMPORTANT:",

        "Apply ONLY the teacher-approved changes listed in the revision brief.",

        "Do not introduce additional changes merely because you would prefer them.",

        "Preserve the original meaning, structure, learning objective, and teaching purpose unless a teacher-approved change requires adjustment.",

        "Keep the revised material appropriate for the original learner profile and intended proficiency level.",

        "",

        "ORIGINAL TEACHER SPECIFICATION:",

        *specification_lines,

        "",

        "TEACHER-APPROVED REVISION BRIEF:",

        revision_brief,

        "",

        "ORIGINAL MATERIAL:",

        original_material,

        "",

        "OUTPUT REQUIREMENT:",

        "Return the complete revised teaching material, not a list or explanation of the changes.",

        "The revised material remains subject to teacher review before classroom use."

    ])



    st.session_state["lensrevise_prompt"] = revision_prompt



    st.divider()

    st.subheader("✨ Teacher-Approved Revision Prompt")



    st.write(

        "Copy this prompt into your preferred generative AI tool. "

        "It contains the original material, teacher specification, "

        "and only the changes approved in LENSFix."

    )



    st.text_area(

        "Revision prompt",

        value=revision_prompt,

        height=500,

        key="lensrevise_prompt_display"

    )



    st.success(

        "Revision prompt ready. LENSRevise has not independently "

        "changed or rewritten the teaching material."

    )



    st.caption(

        "Teacher review and professional judgement remain essential "

        "before the revised material is used in the classroom."

    )





# ============================================================



# PAGE ROUTER



# ============================================================



if st.session_state.page == "home":



    home_page()



elif st.session_state.page == "prompt":



    promptlens_page()



elif st.session_state.page == "langmri":



    langmri_page()



elif st.session_state.page == "lensfix":



    lensfix_page()



elif st.session_state.page == "lensrevise":



    lensrevise_page()


