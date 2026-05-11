import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="AI Launch Readiness Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── LAUNCH STATUS — change this one variable to update entire dashboard theme ──
launch_status = "AT RISK"  # Options: "ON TRACK" | "AT RISK" | "CRITICAL"

if launch_status == "ON TRACK":
    theme_color = "#22c55e"
    theme_bg   = "rgba(34,197,94,0.1)"
    theme_bdr  = "rgba(34,197,94,0.2)"
    hero_bg    = "linear-gradient(135deg,#0a1a0e 0%,#0a1a0e 50%,#0d130a 100%)"
elif launch_status == "CRITICAL":
    theme_color = "#7c3aed"
    theme_bg   = "rgba(124,58,237,0.1)"
    theme_bdr  = "rgba(124,58,237,0.2)"
    hero_bg    = "linear-gradient(135deg,#0d0a1a 0%,#150a2e 50%,#0d0a1a 100%)"
else:
    theme_color = "#EF4444"
    theme_bg   = "rgba(239,68,68,0.1)"
    theme_bdr  = "rgba(239,68,68,0.2)"
    hero_bg    = "linear-gradient(135deg,#0a0e1a 0%,#1a0505 50%,#0d0a0a 100%)"

st.markdown(f"""
<style>
  .main .block-container{{padding-top:0rem;padding-bottom:2rem;padding-left:2rem;padding-right:2rem}}
  .hero{{padding:2rem 2rem 1.5rem 2rem;margin:-1rem -2rem 1.5rem -2rem;
         background:{hero_bg};border-bottom:1px solid {theme_bdr}}}
  .hero-tag{{display:inline-block;font-size:0.68rem;font-weight:700;
             letter-spacing:0.15em;text-transform:uppercase;
             color:{theme_color};background:{theme_bg};
             padding:3px 12px;border-radius:20px;
             border:1px solid {theme_bdr};margin-bottom:0.75rem}}
  .hero-title{{font-size:2.8rem;font-weight:800;color:#ffffff;
               letter-spacing:-1px;line-height:1.05;margin:0 0 0.5rem 0}}
  .hero-title span{{color:{theme_color}}}
  .hero-sub{{font-size:0.88rem;color:rgba(255,255,255,0.45);margin:0;line-height:1.6}}
  .hero-pills{{display:flex;gap:8px;margin-top:1rem;flex-wrap:wrap}}
  .pill{{font-size:0.72rem;font-weight:500;color:rgba(255,255,255,0.55);
         background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
         padding:3px 12px;border-radius:20px}}
  .pill-alert{{font-size:0.72rem;font-weight:700;color:{theme_color};
               background:{theme_bg};border:1px solid {theme_bdr};
               padding:3px 12px;border-radius:20px}}
  .sec-label{{font-size:0.82rem;font-weight:700;letter-spacing:0.06em;
              text-transform:uppercase;color:{theme_color};
              margin-bottom:1rem;padding-bottom:0.6rem;
              border-bottom:1px solid {theme_bdr}}}
  .status-box{{background:{theme_bg};border:1px solid {theme_bdr};
               border-left:4px solid {theme_color};
               border-radius:0 8px 8px 0;padding:1rem 1.25rem;margin-bottom:1rem}}
  .status-title{{font-size:1rem;font-weight:700;color:{theme_color};margin-bottom:4px}}
  .status-sub{{font-size:0.82rem;color:rgba(255,255,255,0.5);line-height:1.6}}
  .modebar{{display:none!important}}
</style>
""", unsafe_allow_html=True)

# ── HARDCODED TASK DATA ──
TASKS_DEFAULT = [
    {"task":"Define business case","phase":"Initiation","owner":"PM","status":"Complete","completion":100,"risk":"Low","note":"Establish launch purpose"},
    {"task":"Identify stakeholders","phase":"Initiation","owner":"PM","status":"Complete","completion":100,"risk":"Low","note":"6 cross-functional teams"},
    {"task":"Define success metrics & KPIs","phase":"Initiation","owner":"PM","status":"Complete","completion":100,"risk":"Low","note":"Accuracy, test pass rate, readiness score"},
    {"task":"Approve project charter","phase":"Initiation","owner":"Sponsor","status":"Complete","completion":100,"risk":"Low","note":"Milestone"},
    {"task":"Define business & technical requirements","phase":"Planning","owner":"Engineering Lead","status":"Complete","completion":100,"risk":"Low","note":"Requirements baseline"},
    {"task":"Create requirements traceability matrix","phase":"Planning","owner":"PM","status":"Complete","completion":100,"risk":"Low","note":"BR/TR mapped to test cases"},
    {"task":"Build WBS and workstream plan","phase":"Planning","owner":"PM","status":"Complete","completion":100,"risk":"Low","note":"Work packages by team"},
    {"task":"Build risk register and RAID log","phase":"Planning","owner":"PM","status":"In Progress","completion":80,"risk":"Medium","note":"Risk ownership assigned"},
    {"task":"Confirm camera hardware supplier","phase":"Hardware","owner":"Supply Chain Lead","status":"Complete","completion":100,"risk":"Medium","note":"Supplier confirmed"},
    {"task":"Camera hardware delivery","phase":"Hardware","owner":"Supply Chain Lead","status":"Delayed","completion":60,"risk":"High","note":"Delivery slipped by 2 days"},
    {"task":"Prepare defect image dataset","phase":"Hardware","owner":"AI/Data Lead","status":"Complete","completion":100,"risk":"Medium","note":"Dataset baseline completed"},
    {"task":"Define AI model validation thresholds","phase":"Hardware","owner":"AI/Data Lead","status":"Complete","completion":100,"risk":"Medium","note":"Accuracy target 92%+"},
    {"task":"Data pipeline readiness check","phase":"Hardware","owner":"Engineering Lead","status":"At Risk","completion":65,"risk":"High","note":"Refresh issue found"},
    {"task":"Install camera station on line","phase":"Integration","owner":"Manufacturing Lead","status":"Delayed","completion":70,"risk":"High","note":"Dependent on hardware arrival"},
    {"task":"Calibrate inspection station","phase":"Integration","owner":"Manufacturing Lead","status":"In Progress","completion":60,"risk":"Medium","note":"Calibration mismatch found"},
    {"task":"Integrate camera feed with pipeline","phase":"Integration","owner":"Engineering Lead","status":"At Risk","completion":50,"risk":"High","note":"Data refresh failing intermittently"},
    {"task":"Validate AI model against test images","phase":"Integration","owner":"AI/Data Lead","status":"In Progress","completion":55,"risk":"High","note":"False negatives above target"},
    {"task":"Design UAT test cases","phase":"UAT","owner":"Quality Lead","status":"Complete","completion":100,"risk":"Medium","note":"Test scenarios finalized"},
    {"task":"Execute UAT cycle 1","phase":"UAT","owner":"Quality Lead","status":"Complete","completion":100,"risk":"Medium","note":"17/20 tests passed (85%)"},
    {"task":"Resolve UAT defects","phase":"UAT","owner":"Engineering Lead","status":"In Progress","completion":60,"risk":"High","note":"Alert trigger failed"},
    {"task":"Execute UAT cycle 2","phase":"UAT","owner":"Quality Lead","status":"Not Started","completion":0,"risk":"High","note":"Pending defect resolution"},
    {"task":"Readiness review","phase":"Launch Prep","owner":"PM","status":"At Risk","completion":60,"risk":"High","note":"Cross-functional delays"},
    {"task":"Risk mitigation","phase":"Launch Prep","owner":"Engineering Lead","status":"In Progress","completion":50,"risk":"High","note":"Pipeline and defect fixes"},
    {"task":"Launch execution","phase":"Go-Live","owner":"PM","status":"Delayed","completion":40,"risk":"High","note":"Controlled rollout planned"},
    {"task":"Monitoring setup","phase":"Go-Live","owner":"Engineering Lead","status":"In Progress","completion":45,"risk":"High","note":"Dashboard alert system"},
]

# CSV-driven: auto-generate on first run, then editable
CSV_PATH = "tasks.csv"
if os.path.exists(CSV_PATH):
    tasks = pd.read_csv(CSV_PATH)
else:
    tasks = pd.DataFrame(TASKS_DEFAULT)
    tasks.to_csv(CSV_PATH, index=False)

PHASES_DEFAULT = [
    {"phase":"Phase 1: Initiation & Requirements","short":"Initiation","completion":100,"status":"Complete","risk":"Low"},
    {"phase":"Phase 2: Planning & Design","short":"Planning","completion":90,"status":"In Progress","risk":"Medium"},
    {"phase":"Phase 3: Hardware & Data Readiness","short":"Hardware","completion":70,"status":"At Risk","risk":"High"},
    {"phase":"Phase 4: Installation & Integration","short":"Integration","completion":60,"status":"At Risk","risk":"High"},
    {"phase":"Phase 5: UAT & Quality Validation","short":"UAT","completion":50,"status":"At Risk","risk":"High"},
    {"phase":"Phase 6: Launch Preparation","short":"Launch Prep","completion":60,"status":"At Risk","risk":"High"},
    {"phase":"Phase 7: Go-Live & Monitoring","short":"Go-Live","completion":45,"status":"Delayed","risk":"High"},
]
phases = pd.DataFrame(PHASES_DEFAULT)

# ── METRICS ──
overall_completion = round(tasks["completion"].mean())
at_risk_tasks   = len(tasks[tasks["status"].isin(["At Risk","Delayed"])])
complete_tasks  = len(tasks[tasks["status"] == "Complete"])
high_risk_tasks = len(tasks[tasks["risk"] == "High"])
uat_pass_rate   = 85

# ── HERO ──
st.markdown(f"""
<div class='hero'>
  <div class='hero-tag'>Technical Program Management · Case Study</div>
  <p class='hero-title'>AI Launch Readiness<br><span>Command Center</span></p>
  <p class='hero-sub'>
    End-to-end program management simulation for an AI-powered defect
    detection system deployment in a manufacturing environment ·
    Hybrid Agile-Waterfall methodology
  </p>
  <div class='hero-pills'>
    <span class='pill'>May – Sep 2026 · 19 Weeks</span>
    <span class='pill'>7 Phases · 25 Tasks · 7 Milestones</span>
    <span class='pill'>6 Cross-Functional Teams</span>
    <span class='pill'>Smartsheet · Notion · RAID Log</span>
    <span class='pill-alert'>⚠ Launch Status: {launch_status}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── KPI ROW ──
k1,k2,k3,k4,k5,k6 = st.columns(6)
k1.metric("Overall Completion", f"{overall_completion}%", "-26% from target")
k2.metric("Tasks Complete", f"{complete_tasks}/25")
k3.metric("At Risk / Delayed", f"{at_risk_tasks}", delta="needs action", delta_color="inverse")
k4.metric("UAT Pass Rate", f"{uat_pass_rate}%", "Target: 95%", delta_color="inverse")
k5.metric("High Risk Tasks", f"{high_risk_tasks}", delta="immediate action", delta_color="inverse")
k6.metric("AI Accuracy Target", "92%+", "threshold set")

st.markdown("---")

# ── STATUS ALERT ──
st.markdown(f"""
<div class='status-box'>
  <div class='status-title'>⚠ Executive Status: {launch_status} — Go/No-Go Recommendation: NO-GO</div>
  <div class='status-sub'>Supply chain delays in hardware delivery, integration failures in the
  camera-dashboard pipeline, and a UAT pass rate of 85% (below 95% threshold) collectively
  prevent launch readiness. Immediate mitigation required across 3 workstreams.</div>
</div>
""", unsafe_allow_html=True)

# ── ROW 1: PHASE COMPLETION + STATUS PIE ──
r1c1, r1c2 = st.columns([3,2])

STATUS_COLORS = {
    "Complete":"#22c55e","In Progress":"#3b82f6",
    "At Risk":"#ef4444","Delayed":"#f97316","Not Started":"#6b7280"
}

with r1c1:
    st.markdown("<p class='sec-label'>Phase Completion Overview</p>", unsafe_allow_html=True)
    fig1 = go.Figure()
    for _, row in phases.iterrows():
        color = STATUS_COLORS.get(row["status"], "#6b7280")
        fig1.add_trace(go.Bar(
            x=[row["completion"]], y=[row["short"]],
            orientation='h', marker_color=color,
            text=f"{row['completion']}% — {row['status']}",
            textposition='outside', showlegend=False,
            hovertemplate=f"<b>{row['phase']}</b><br>Completion: {row['completion']}%<br>Status: {row['status']}<br>Risk: {row['risk']}<extra></extra>"
        ))
    fig1.update_layout(
        height=320, margin=dict(l=0,r=130,t=5,b=0),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(title='% Completion', range=[0,135], showgrid=False),
        yaxis=dict(title='', categoryorder='array',
                   categoryarray=phases['short'].tolist()[::-1]),
    )
    st.plotly_chart(fig1, use_container_width=True)

with r1c2:
    st.markdown("<p class='sec-label'>Task Status Distribution</p>", unsafe_allow_html=True)
    sc = tasks["status"].value_counts().reset_index()
    sc.columns = ["status","count"]
    fig2 = px.pie(sc, values='count', names='status', color='status',
                  color_discrete_map=STATUS_COLORS, hole=0.55)
    fig2.update_layout(height=320, margin=dict(l=0,r=0,t=5,b=30),
                       paper_bgcolor='rgba(0,0,0,0)',
                       legend=dict(orientation='h',y=-0.2,title=None))
    fig2.update_traces(textinfo='percent',
        hovertemplate="<b>%{label}</b><br>Tasks: %{value}<br>Share: %{percent}<extra></extra>")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── ROW 2: RISK + UAT ──
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown("<p class='sec-label'>Risk Distribution by Workstream</p>", unsafe_allow_html=True)
    rd = tasks.groupby(['phase','risk']).size().reset_index(name='count')
    fig3 = px.bar(rd, x='phase', y='count', color='risk',
                  color_discrete_map={'High':'#ef4444','Medium':'#f97316','Low':'#22c55e'},
                  barmode='stack',
                  labels={'count':'Task Count','phase':'Phase','risk':'Risk Level'})
    fig3.update_layout(
        height=300, margin=dict(l=0,r=0,t=5,b=0),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, tickangle=0),
        yaxis=dict(gridcolor='rgba(128,128,128,0.1)'),
        legend=dict(orientation='h',y=1.1,title=None)
    )
    st.plotly_chart(fig3, use_container_width=True)

with r2c2:
    st.markdown("<p class='sec-label'>UAT Quality Validation Progress</p>", unsafe_allow_html=True)
    uat = pd.DataFrame([
        {"cycle":"UAT Cycle 1","planned":20,"passed":17,"failed":3},
        {"cycle":"UAT Cycle 2","planned":20,"passed":0,"failed":0},
    ])
    fig4 = go.Figure()
    fig4.add_trace(go.Bar(name='Planned', x=uat['cycle'], y=uat['planned'],
                          marker_color='rgba(59,130,246,0.3)',
                          text=uat['planned'], textposition='outside'))
    fig4.add_trace(go.Bar(name='Passed', x=uat['cycle'], y=uat['passed'],
                          marker_color='#22c55e',
                          text=uat['passed'], textposition='outside'))
    fig4.add_trace(go.Bar(name='Failed', x=uat['cycle'], y=uat['failed'],
                          marker_color='#ef4444',
                          text=uat['failed'], textposition='outside'))
    fig4.add_hline(y=19, line_dash="dot", line_color="#ef4444",
                   annotation_text="95% threshold (19/20)",
                   annotation_position="top right")
    fig4.update_layout(
        height=300, barmode='group',
        margin=dict(l=0,r=0,t=5,b=0),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='rgba(128,128,128,0.1)',title='Test Cases'),
        legend=dict(orientation='h',y=1.1,title=None)
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── TASK REGISTER ──
st.markdown("<p class='sec-label'>Full Task Register — Live Program Status</p>", unsafe_allow_html=True)

col_f1, col_f2 = st.columns(2)
with col_f1:
    phase_filter = st.selectbox("Filter by Phase",
        ["All Phases"] + sorted(tasks['phase'].unique().tolist()))
with col_f2:
    status_filter = st.multiselect("Filter by Status",
        options=tasks['status'].unique().tolist(),
        default=tasks['status'].unique().tolist())

filtered = tasks.copy()
if phase_filter != "All Phases":
    filtered = filtered[filtered['phase'] == phase_filter]
filtered = filtered[filtered['status'].isin(status_filter)]

def color_status(val):
    return {
        'Complete':    'background-color:rgba(34,197,94,0.15);color:#16a34a',
        'At Risk':     'background-color:rgba(239,68,68,0.15);color:#dc2626',
        'Delayed':     'background-color:rgba(249,115,22,0.15);color:#ea580c',
        'In Progress': 'background-color:rgba(59,130,246,0.15);color:#2563eb',
        'Not Started': 'background-color:rgba(107,114,128,0.1);color:#6b7280',
    }.get(val,'')

def color_risk(val):
    return {
        'High':   'background-color:rgba(239,68,68,0.15);color:#dc2626',
        'Medium': 'background-color:rgba(249,115,22,0.1);color:#ea580c',
        'Low':    'background-color:rgba(34,197,94,0.1);color:#16a34a',
    }.get(val,'')

display = filtered[['task','phase','owner','status','completion','risk','note']].copy()
display.columns = ['Task','Phase','Owner','Status','% Done','Risk','Notes']
st.dataframe(
    display.style
    .map(color_status, subset=['Status'])
    .map(color_risk,   subset=['Risk']),
    use_container_width=True, height=350
)

st.markdown("---")

# ── RAID LOG ──
st.markdown("<p class='sec-label'>RAID Log — Active Items</p>", unsafe_allow_html=True)

raid = pd.DataFrame([
    {"Type":"Risk",       "Description":"Supplier delay in camera delivery",          "Impact":"High",   "Owner":"Supply Lead",  "Action":"Activate backup vendor, expedite logistics",       "Status":"Open"},
    {"Type":"Risk",       "Description":"AI model accuracy below 95% threshold",      "Impact":"High",   "Owner":"AI Lead",      "Action":"Increase training dataset, retrain model",          "Status":"In Progress"},
    {"Type":"Risk",       "Description":"Integration failure — camera to pipeline",   "Impact":"High",   "Owner":"Eng Lead",     "Action":"Run integration testing cycles, debug",             "Status":"In Progress"},
    {"Type":"Issue",      "Description":"Data pipeline refresh failing intermittently","Impact":"High",   "Owner":"Eng Lead",     "Action":"Debug pipeline, optimize performance",              "Status":"In Progress"},
    {"Type":"Issue",      "Description":"High defect rate — false negatives",         "Impact":"High",   "Owner":"QA Lead",      "Action":"Add validation cycles, improve testing",            "Status":"In Progress"},
    {"Type":"Assumption", "Description":"Vendor delivers components within 2 weeks",  "Impact":"Medium", "Owner":"Supply Lead",  "Action":"Track vendor timelines",                           "Status":"Validated"},
    {"Type":"Dependency", "Description":"Integration depends on hardware setup",      "Impact":"High",   "Owner":"Mfg Lead",     "Action":"Ensure timely installation and testing",            "Status":"Open"},
    {"Type":"Dependency", "Description":"UAT depends on model validation",            "Impact":"Medium", "Owner":"AI Lead",      "Action":"Align testing schedule with QA team",              "Status":"Open"},
])

def c_type(v):
    return {'Risk':'background-color:rgba(239,68,68,0.1);color:#dc2626',
            'Issue':'background-color:rgba(249,115,22,0.1);color:#ea580c',
            'Dependency':'background-color:rgba(59,130,246,0.1);color:#2563eb',
            'Assumption':'background-color:rgba(34,197,94,0.1);color:#16a34a'}.get(v,'')
def c_imp(v):
    return {'High':'background-color:rgba(239,68,68,0.15);color:#dc2626',
            'Medium':'background-color:rgba(249,115,22,0.1);color:#ea580c'}.get(v,'')

st.dataframe(
    raid.style.map(c_type,subset=['Type']).map(c_imp,subset=['Impact']),
    use_container_width=True, height=280
)

st.markdown("---")

# ── LESSONS LEARNED ──
st.markdown("<p class='sec-label'>Lessons Learned</p>", unsafe_allow_html=True)

lessons = [
    ("Visibility > execution speed",
     "The dashboard revealed delays invisible in status meetings. Early visibility enabled faster intervention."),
    ("Cross-functional dependencies = biggest risk",
     "Supply chain delays cascaded into manufacturing, integration, then UAT. Dependencies must be managed proactively."),
    ("Early testing prevents late-stage failure",
     "UAT defects discovered in Cycle 1 could have been caught earlier with integration testing in Phase 3."),
    ("Data-driven go/no-go decisions",
     "Quantified KPIs (85% vs 95% target) enabled objective launch assessment rather than opinion-based decisions."),
    ("Risk mitigation must be proactive",
     "5 of 8 RAID items were reactive. Risk triggers should be defined and monitored before issues materialise."),
]

l1, l2 = st.columns(2)
for i, (title, desc) in enumerate(lessons):
    col = l1 if i % 2 == 0 else l2
    with col:
        st.markdown(f"""
        <div style='padding:0.85rem 1rem;background:{theme_bg};
             border-left:2px solid {theme_color};
             border-radius:0 6px 6px 0;margin-bottom:8px'>
          <div style='font-size:13px;font-weight:600;
               color:var(--color-text-primary);margin-bottom:3px'>{title}</div>
          <div style='font-size:12px;color:var(--color-text-secondary);
               line-height:1.6'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
<p style='font-size:0.78rem;opacity:0.3;'>
Akshada Karade &nbsp;·&nbsp; MS Engineering Management, UMass Amherst &nbsp;·&nbsp;
Technical PM Case Study &nbsp;·&nbsp;
Tools: Smartsheet · Notion · Python · Streamlit
</p>
""", unsafe_allow_html=True)