import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

st.set_page_config(
    page_title="AI Launch Readiness Command Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

launch_status = "AT RISK"

if launch_status == "ON TRACK":
    tc="#22c55e"; tbg="rgba(34,197,94,0.1)"; tbdr="rgba(34,197,94,0.2)"
    hero_bg="linear-gradient(135deg,#0a1a0e 0%,#0d1a0e 100%)"
elif launch_status == "CRITICAL":
    tc="#7c3aed"; tbg="rgba(124,58,237,0.1)"; tbdr="rgba(124,58,237,0.2)"
    hero_bg="linear-gradient(135deg,#0d0a1a 0%,#150a2e 100%)"
else:
    tc="#EF4444"; tbg="rgba(239,68,68,0.1)"; tbdr="rgba(239,68,68,0.2)"
    hero_bg="linear-gradient(135deg,#0a0e1a 0%,#1a0808 100%)"

STATUS_COLORS = {
    "Complete":"#22c55e","In Progress":"#3b82f6",
    "At Risk":"#ef4444","Delayed":"#f97316","Not Started":"#6b7280"
}

st.markdown(f"""
<style>
.main .block-container{{padding-top:0;padding-bottom:2rem;
  padding-left:2rem;padding-right:2rem}}
.hero{{padding:2.5rem 2rem 2rem;margin:-1rem -2rem 2rem -2rem;
  background:{hero_bg};border-bottom:1px solid {tbdr}}}
.hero-eyebrow{{font-size:0.68rem;font-weight:700;letter-spacing:0.18em;
  text-transform:uppercase;color:{tc};background:{tbg};
  padding:3px 14px;border-radius:20px;border:1px solid {tbdr};
  display:inline-block;margin-bottom:1rem}}
.hero-sub{{font-size:0.9rem;color:rgba(255,255,255,0.45);
  line-height:1.7;margin:0.5rem 0 1.25rem}}
.hero-pills{{display:flex;gap:8px;flex-wrap:wrap}}
.pill{{font-size:0.72rem;color:rgba(255,255,255,0.5);
  background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);
  padding:3px 12px;border-radius:20px}}
.pill-hot{{font-size:0.72rem;font-weight:700;color:{tc};
  background:{tbg};border:1px solid {tbdr};padding:3px 12px;border-radius:20px}}
.sec{{font-size:0.78rem;font-weight:700;letter-spacing:0.08em;
  text-transform:uppercase;color:{tc};margin-bottom:0.9rem;
  padding-bottom:0.6rem;border-bottom:1px solid {tbdr}}}
.alert-box{{background:{tbg};border:1px solid {tbdr};
  border-left:4px solid {tc};border-radius:0 8px 8px 0;
  padding:1rem 1.25rem;margin-bottom:1.5rem}}
.alert-title{{font-size:1rem;font-weight:700;color:{tc};margin-bottom:4px}}
.alert-sub{{font-size:0.83rem;color:rgba(255,255,255,0.5);line-height:1.65}}
.modebar{{display:none!important}}
.sidebar-section{{font-size:0.68rem;font-weight:700;letter-spacing:0.12em;
  text-transform:uppercase;color:{tc};margin:1rem 0 0.5rem}}
</style>
""", unsafe_allow_html=True)

# ══════════════════ DATA ══════════════════
TASKS_DATA = [
    {"task":"Define business case and launch objective","phase":"Initiation","owner":"PM","workstream":"Program","status":"Complete","completion":100,"risk":"Low","start":"2026-05-04","end":"2026-05-05","duration":"2d","note":"Establish launch purpose"},
    {"task":"Identify stakeholders and ownership model","phase":"Initiation","owner":"PM","workstream":"Program","status":"Complete","completion":100,"risk":"Low","start":"2026-05-06","end":"2026-05-07","duration":"2d","note":"Engineering, AI/Data, Quality, Manufacturing, Supply Chain, Ops"},
    {"task":"Define success metrics and KPIs","phase":"Initiation","owner":"PM","workstream":"Program","status":"Complete","completion":100,"risk":"Low","start":"2026-05-08","end":"2026-05-11","duration":"2d","note":"Accuracy, test pass rate, readiness score"},
    {"task":"Approve project charter","phase":"Initiation","owner":"Sponsor","workstream":"Program","status":"Complete","completion":100,"risk":"Low","start":"2026-05-12","end":"2026-05-15","duration":"4d","note":"Milestone — signed off by Sponsor"},
    {"task":"Define business and technical requirements","phase":"Planning","owner":"Engineering Lead","workstream":"Engineering","status":"Complete","completion":100,"risk":"Low","start":"2026-05-18","end":"2026-05-20","duration":"3d","note":"Requirements baseline — functional & non-functional"},
    {"task":"Create requirements traceability matrix","phase":"Planning","owner":"PM","workstream":"Program","status":"Complete","completion":100,"risk":"Low","start":"2026-06-01","end":"2026-06-02","duration":"2d","note":"BR/TR mapped to test cases"},
    {"task":"Build WBS and workstream plan","phase":"Planning","owner":"PM","workstream":"Program","status":"Complete","completion":100,"risk":"Low","start":"2026-05-21","end":"2026-05-22","duration":"2d","note":"Work packages assigned by team"},
    {"task":"Build risk register and RAID log","phase":"Planning","owner":"PM","workstream":"Program","status":"In Progress","completion":80,"risk":"Medium","start":"2026-06-03","end":"2026-06-05","duration":"3d","note":"Risk ownership assigned — 8 risks logged"},
    {"task":"Confirm camera hardware supplier","phase":"Hardware","owner":"Supply Chain Lead","workstream":"Supply Chain","status":"Complete","completion":100,"risk":"Medium","start":"2026-05-25","end":"2026-05-29","duration":"5d","note":"Supplier confirmed — backup identified"},
    {"task":"Camera hardware delivery","phase":"Hardware","owner":"Supply Chain Lead","workstream":"Supply Chain","status":"Delayed","completion":60,"risk":"High","start":"2026-05-22","end":"2026-05-28","duration":"5d","note":"Delivery slipped by 2 days — cascading impact"},
    {"task":"Prepare defect image dataset","phase":"Hardware","owner":"AI/Data Lead","workstream":"AI/Data","status":"Complete","completion":100,"risk":"Medium","start":"2026-05-25","end":"2026-06-03","duration":"8d","note":"Dataset baseline completed — 2,400+ images"},
    {"task":"Define AI model validation thresholds","phase":"Hardware","owner":"AI/Data Lead","workstream":"AI/Data","status":"Complete","completion":100,"risk":"Medium","start":"2026-06-01","end":"2026-06-03","duration":"3d","note":"Accuracy target raised to 92%+ via CR-C1"},
    {"task":"Data pipeline readiness check","phase":"Hardware","owner":"Engineering Lead","workstream":"Engineering","status":"At Risk","completion":65,"risk":"High","start":"2026-06-15","end":"2026-06-18","duration":"4d","note":"Refresh issue found — intermittent failure"},
    {"task":"Install camera station on line","phase":"Integration","owner":"Manufacturing Lead","workstream":"Manufacturing","status":"Delayed","completion":70,"risk":"High","start":"2026-06-15","end":"2026-06-19","duration":"5d","note":"Dependent on hardware arrival — blocked"},
    {"task":"Calibrate inspection station","phase":"Integration","owner":"Manufacturing Lead","workstream":"Manufacturing","status":"In Progress","completion":60,"risk":"Medium","start":"2026-06-19","end":"2026-06-23","duration":"3d","note":"Calibration mismatch found — rework in progress"},
    {"task":"Integrate camera feed with dashboard pipeline","phase":"Integration","owner":"Engineering Lead","workstream":"Engineering","status":"At Risk","completion":50,"risk":"High","start":"2026-06-03","end":"2026-06-08","duration":"4d","note":"Data refresh failing intermittently"},
    {"task":"Validate AI model against test images","phase":"Integration","owner":"AI/Data Lead","workstream":"AI/Data","status":"In Progress","completion":55,"risk":"High","start":"2026-06-25","end":"2026-06-29","duration":"3d","note":"False negatives above acceptable threshold"},
    {"task":"Design UAT test cases","phase":"UAT","owner":"Quality Lead","workstream":"Quality","status":"Complete","completion":100,"risk":"Medium","start":"2026-06-22","end":"2026-06-23","duration":"2d","note":"20 test scenarios finalized across 5 modules"},
    {"task":"Execute UAT cycle 1","phase":"UAT","owner":"Quality Lead","workstream":"Quality","status":"Complete","completion":100,"risk":"Medium","start":"2026-06-09","end":"2026-06-11","duration":"3d","note":"17/20 tests passed (85%) — below 95% threshold"},
    {"task":"Resolve UAT defects","phase":"UAT","owner":"Engineering Lead","workstream":"Engineering","status":"In Progress","completion":60,"risk":"High","start":"2026-06-30","end":"2026-07-02","duration":"3d","note":"Alert trigger failed — 3 defects open"},
    {"task":"Execute UAT cycle 2","phase":"UAT","owner":"Quality Lead","workstream":"Quality","status":"Not Started","completion":0,"risk":"High","start":"2026-07-23","end":"2026-07-24","duration":"2d","note":"Blocked — pending defect resolution"},
    {"task":"Readiness review","phase":"Launch Prep","owner":"PM","workstream":"Program","status":"At Risk","completion":60,"risk":"High","start":"2026-08-19","end":"2026-08-24","duration":"4d","note":"Cross-functional delays impacting readiness"},
    {"task":"Risk mitigation actions","phase":"Launch Prep","owner":"Engineering Lead","workstream":"Engineering","status":"In Progress","completion":50,"risk":"High","start":"2026-08-25","end":"2026-09-01","duration":"6d","note":"Pipeline and defect fixes in progress"},
    {"task":"Launch execution","phase":"Go-Live","owner":"PM","workstream":"Operations","status":"Delayed","completion":40,"risk":"High","start":"2026-09-02","end":"2026-09-08","duration":"5d","note":"Controlled rollout — limited production volume"},
    {"task":"Monitoring setup","phase":"Go-Live","owner":"Engineering Lead","workstream":"Engineering","status":"In Progress","completion":45,"risk":"High","start":"2026-09-09","end":"2026-09-15","duration":"5d","note":"Dashboard alert system and monitoring setup"},
]

CSV_PATH = "tasks.csv"
if os.path.exists(CSV_PATH):
    tasks = pd.read_csv(CSV_PATH)
else:
    tasks = pd.DataFrame(TASKS_DATA)
    tasks.to_csv(CSV_PATH, index=False)

phases = pd.DataFrame([
    {"short":"Initiation","completion":100,"status":"Complete","risk":"Low","phase":"Phase 1: Initiation & Requirements","milestone":"Initiation & Requirements Complete"},
    {"short":"Planning","completion":90,"status":"In Progress","risk":"Medium","phase":"Phase 2: Planning & Design","milestone":"Planning & Design Complete"},
    {"short":"Hardware","completion":70,"status":"At Risk","risk":"High","phase":"Phase 3: Hardware & Data Readiness","milestone":"Hardware & Data Readiness Complete"},
    {"short":"Integration","completion":60,"status":"At Risk","risk":"High","phase":"Phase 4: Installation & Integration","milestone":"Installation & Integration Complete"},
    {"short":"UAT","completion":50,"status":"At Risk","risk":"High","phase":"Phase 5: UAT & Quality Validation","milestone":"UAT & Quality Validation / Launch Ready"},
    {"short":"Launch Prep","completion":60,"status":"At Risk","risk":"High","phase":"Phase 6: Launch Preparation","milestone":"Launch Preparation Complete"},
    {"short":"Go-Live","completion":45,"status":"Delayed","risk":"High","phase":"Phase 7: Go-Live & Monitoring","milestone":"Go-Live & Monitoring Complete"},
])

risk_register = pd.DataFrame([
    {"id":"R1","risk":"Supplier delay in camera delivery","probability":5,"impact":5,"score":25,"owner":"Supply Lead","status":"Open","mitigation":"Activate backup vendor, expedite logistics"},
    {"id":"R2","risk":"AI model accuracy below 95% threshold","probability":4,"impact":5,"score":20,"owner":"AI Lead","status":"In Progress","mitigation":"Increase training dataset and retrain model"},
    {"id":"R3","risk":"System integration failure between modules","probability":4,"impact":5,"score":20,"owner":"Eng Lead","status":"In Progress","mitigation":"Run integration testing cycles and debug"},
    {"id":"R4","risk":"High defect rate in AI predictions","probability":3,"impact":4,"score":12,"owner":"QA Lead","status":"In Progress","mitigation":"Add validation cycles, improve test coverage"},
    {"id":"R5","risk":"Data pipeline failure","probability":3,"impact":4,"score":12,"owner":"Eng Lead","status":"In Progress","mitigation":"Debug pipeline, optimize performance"},
    {"id":"R6","risk":"Resource constraint in QA team","probability":2,"impact":3,"score":6,"owner":"QA Lead","status":"Open","mitigation":"Escalate to PMO for resource reallocation"},
    {"id":"R7","risk":"Unexpected hardware failure","probability":2,"impact":5,"score":10,"owner":"Mfg Lead","status":"Open","mitigation":"Maintain spare components, warranty coverage"},
    {"id":"R8","risk":"UAT delay due to dependency issues","probability":3,"impact":4,"score":12,"owner":"Ops Lead","status":"Open","mitigation":"Align UAT schedule with defect resolution plan"},
])

change_log = pd.DataFrame([
    {"id":"CR-C1","request":"Increase AI accuracy threshold from 85% to 90%","impact":"High","decision":"Approved","owner":"AI Lead","rationale":"Industry standard requires higher accuracy for manufacturing"},
    {"id":"CR-C2","request":"Add additional UAT cycle (Cycle 2)","impact":"Medium","decision":"Approved","owner":"QA Lead","rationale":"Cycle 1 results below threshold — extra validation required"},
    {"id":"CR-C3","request":"Introduce backup hardware supplier","impact":"High","decision":"Approved","owner":"Supply Lead","rationale":"Primary supplier delay risk — mitigation approved"},
    {"id":"CR-C4","request":"Extend integration timeline by 1 week","impact":"High","decision":"Approved","owner":"Eng Lead","rationale":"Hardware delay cascaded into integration phase"},
    {"id":"CR-C5","request":"Add real-time dashboard monitoring","impact":"Medium","decision":"Approved","owner":"Ops Lead","rationale":"Visibility requirement identified during Phase 3 review"},
    {"id":"CR-C6","request":"Reduce scope of non-critical features","impact":"Low","decision":"Rejected","owner":"Product Manager","rationale":"Core functionality cannot be descoped — affects MVP"},
    {"id":"CR-C7","request":"Increase test coverage by 20%","impact":"Medium","decision":"Approved","owner":"QA Lead","rationale":"Risk mitigation for UAT Cycle 2 quality assurance"},
])

raid = pd.DataFrame([
    {"type":"Risk","description":"Supplier delay in camera delivery","impact":"High","owner":"Supply Lead","action":"Activate backup vendor, expedite logistics","status":"Open"},
    {"type":"Risk","description":"AI model accuracy below 95% threshold","impact":"High","owner":"AI Lead","action":"Increase training dataset, retrain model","status":"In Progress"},
    {"type":"Risk","description":"Integration failure — camera to pipeline","impact":"High","owner":"Eng Lead","action":"Run integration testing cycles, debug","status":"In Progress"},
    {"type":"Issue","description":"Data pipeline refresh failing intermittently","impact":"High","owner":"Eng Lead","action":"Debug pipeline, optimize performance","status":"In Progress"},
    {"type":"Issue","description":"High defect rate — false negatives above target","impact":"High","owner":"QA Lead","action":"Add validation cycles, improve testing","status":"In Progress"},
    {"type":"Assumption","description":"Vendor delivers components within 2 weeks","impact":"Medium","owner":"Supply Lead","action":"Track vendor timelines, confirm milestones","status":"Validated"},
    {"type":"Assumption","description":"Test environment stable for UAT","impact":"Medium","owner":"QA Lead","action":"Monitor environment readiness","status":"Validated"},
    {"type":"Dependency","description":"System integration depends on hardware setup","impact":"High","owner":"Mfg Lead","action":"Ensure timely installation and testing","status":"Open"},
    {"type":"Dependency","description":"UAT depends on model validation completion","impact":"Medium","owner":"AI Lead","action":"Align testing schedule with QA team","status":"Open"},
])

stakeholders = pd.DataFrame([
    {"stakeholder":"Engineering Team","role":"System development & integration","interest":3,"influence":3,"engagement":"Active"},
    {"stakeholder":"AI/Data Team","role":"Model development & validation","interest":3,"influence":3,"engagement":"Active"},
    {"stakeholder":"Manufacturing","role":"Hardware installation & calibration","interest":3,"influence":2,"engagement":"Active"},
    {"stakeholder":"Supply Chain","role":"Hardware procurement & delivery","interest":2,"influence":3,"engagement":"Monitor"},
    {"stakeholder":"Quality Team","role":"UAT testing & defect validation","interest":3,"influence":3,"engagement":"Active"},
    {"stakeholder":"Operations/Sponsor","role":"Launch decision & go/no-go authority","interest":3,"influence":3,"engagement":"Inform"},
])

# Add small jitter to separate overlapping stakeholder points
np.random.seed(42)
stakeholders['int_j'] = stakeholders['interest'] + np.random.uniform(-0.15, 0.15, len(stakeholders))
stakeholders['inf_j'] = stakeholders['influence'] + np.random.uniform(-0.15, 0.15, len(stakeholders))

# ══════════════════ METRICS ══════════════════
overall = round(tasks["completion"].mean())
done    = len(tasks[tasks["status"]=="Complete"])
at_risk = len(tasks[tasks["status"].isin(["At Risk","Delayed"])])
hi_risk = len(tasks[tasks["risk"]=="High"])

# ══════════════════ SIDEBAR ══════════════════
with st.sidebar:
    st.markdown(f"<p class='sidebar-section'>Project Intelligence</p>", unsafe_allow_html=True)
    for label, val, sub in [
        ("Overall Completion", f"{overall}%", "weighted average"),
        ("Tasks Complete", f"{done}/25", "of total tasks"),
        ("At Risk / Delayed", f"{at_risk}", "need action"),
        ("High Risk Tasks", f"{hi_risk}", "immediate attention"),
        ("UAT Pass Rate", "85%", "target: 95%"),
        ("Change Requests", "7 CRs", "6 approved · 1 rejected"),
        ("RAID Items", "9", "risks, issues, deps"),
    ]:
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
             border-radius:6px;padding:0.65rem 0.85rem;margin-bottom:6px'>
          <div style='font-size:0.62rem;text-transform:uppercase;letter-spacing:0.08em;
               color:rgba(255,255,255,0.4);margin-bottom:2px'>{label}</div>
          <div style='font-size:1.2rem;font-weight:700;color:{tc};line-height:1'>{val}</div>
          <div style='font-size:0.65rem;color:rgba(255,255,255,0.3);margin-top:2px'>{sub}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<p class='sidebar-section'>Task Filters</p>", unsafe_allow_html=True)

    phase_opts = ["All Phases"] + sorted(tasks['phase'].unique().tolist())
    phase_filter = st.selectbox("Phase", phase_opts, label_visibility="collapsed")

    status_filter = st.multiselect(
        "Status",
        options=tasks['status'].unique().tolist(),
        default=tasks['status'].unique().tolist()
    )

    workstream_filter = st.multiselect(
        "Workstream",
        options=sorted(tasks['workstream'].unique().tolist()),
        default=sorted(tasks['workstream'].unique().tolist())
    )

    st.markdown("---")
    st.markdown(f"<p style='font-size:0.65rem;opacity:0.35;line-height:1.7;'>"
                f"Akshada Karade<br>MS Engineering Management<br>"
                f"UMass Amherst</p>", unsafe_allow_html=True)

# Apply filters
filtered = tasks.copy()
if phase_filter != "All Phases":
    filtered = filtered[filtered['phase'] == phase_filter]
filtered = filtered[
    filtered['status'].isin(status_filter) &
    filtered['workstream'].isin(workstream_filter)
]

# ══════════════════ HERO ══════════════════
st.markdown(f"""
<div class='hero'>
  <div class='hero-eyebrow'>Technical Program Management · Manufacturing AI · Case Study</div>
  <p style='font-size:52px;font-weight:900;color:#fff;letter-spacing:-2px;
     line-height:1.0;margin:0 0 0.4rem;font-family:Arial Black,sans-serif;'>
    AI Launch Readiness<br>
    <span style='color:{tc};'>Command Center</span>
  </p>
  <p class='hero-sub'>
    End-to-end technical program simulation for deploying an AI-powered visual
    defect detection system in a manufacturing environment — managed using
    Hybrid Agile-Waterfall methodology across 6 cross-functional teams.
  </p>
  <div class='hero-pills'>
    <span class='pill'>May 4 – Sep 15, 2026 · 19 Weeks</span>
    <span class='pill'>7 Phases · 25 Tasks · 7 Milestones</span>
    <span class='pill'>6 Workstreams · 6 Stakeholder Groups</span>
    <span class='pill'>Smartsheet · Notion · RAID · Risk Register</span>
    <span class='pill-hot'>⚠ Launch Status: {launch_status}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════ TABS ══════════════════
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Program Overview",
    "Task Register",
    "RAID Log",
    "Risk Register",
    "Change Control",
    "Stakeholders"
])

# ══════ TAB 1: OVERVIEW ══════
with tab1:
    st.markdown(f"""
    <div class='alert-box'>
      <div class='alert-title'>⚠ Executive Status: {launch_status} — Go/No-Go Recommendation: NO-GO</div>
      <div class='alert-sub'>Three compounding issues prevent launch: (1) Camera hardware delivery slipped 2 days, cascading into Phase 4 installation. (2) Data pipeline refresh failing intermittently — blocking camera-dashboard integration. (3) UAT Cycle 1 pass rate of 85% falls below the 95% acceptance threshold. Immediate cross-functional escalation required before re-assessment.</div>
    </div>
    """, unsafe_allow_html=True)

    r1, r2 = st.columns([3, 2])
    with r1:
        st.markdown("<p class='sec'>Phase Completion & Status</p>", unsafe_allow_html=True)
        fig1 = go.Figure()
        for _, row in phases.iterrows():
            col = STATUS_COLORS.get(row["status"], "#6b7280")
            fig1.add_trace(go.Bar(
                x=[row["completion"]], y=[row["short"]],
                orientation='h', marker_color=col,
                text=f"{row['completion']}% — {row['status']}",
                textposition='outside', showlegend=False,
                hovertemplate=f"<b>{row['phase']}</b><br>Completion: {row['completion']}%<br>Status: {row['status']}<br>Risk: {row['risk']}<br>Milestone: {row['milestone']}<extra></extra>"
            ))
        fig1.update_layout(
            height=340, margin=dict(l=0, r=140, t=5, b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='% Completion', range=[0,145], showgrid=False),
            yaxis=dict(title='', categoryorder='array',
                       categoryarray=phases['short'].tolist()[::-1])
        )
        st.plotly_chart(fig1, use_container_width=True)

    with r2:
        st.markdown("<p class='sec'>Task Status Distribution</p>", unsafe_allow_html=True)
        sc = tasks["status"].value_counts().reset_index()
        sc.columns = ["status","count"]
        fig2 = px.pie(sc, values='count', names='status', color='status',
                      color_discrete_map=STATUS_COLORS, hole=0.58)
        fig2.update_layout(height=340, margin=dict(l=0,r=0,t=5,b=30),
                           paper_bgcolor='rgba(0,0,0,0)',
                           legend=dict(orientation='h',y=-0.2,title=None))
        fig2.update_traces(textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Tasks: %{value}<extra></extra>")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    r2a, r2b = st.columns(2)

    with r2a:
        st.markdown("<p class='sec'>Risk Distribution by Workstream</p>", unsafe_allow_html=True)
        rd = tasks.groupby(['phase','risk']).size().reset_index(name='count')
        fig3 = px.bar(rd, x='phase', y='count', color='risk',
                      color_discrete_map={'High':'#ef4444','Medium':'#f97316','Low':'#22c55e'},
                      barmode='stack')
        fig3.update_layout(
            height=300, margin=dict(l=0,r=0,t=5,b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickangle=0, title=''),
            yaxis=dict(gridcolor='rgba(128,128,128,0.1)', title='Task Count'),
            legend=dict(orientation='h',y=1.1,title=None)
        )
        st.plotly_chart(fig3, use_container_width=True)

    with r2b:
        st.markdown("<p class='sec'>UAT Quality Validation — Cycle Results</p>", unsafe_allow_html=True)
        uat = pd.DataFrame([
            {"cycle":"Cycle 1\n(Complete)","planned":20,"passed":17,"failed":3},
            {"cycle":"Cycle 2\n(Pending)","planned":20,"passed":0,"failed":0},
        ])
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            name='Planned', x=uat['cycle'], y=uat['planned'],
            marker_color='rgba(59,130,246,0.3)',
            text=uat['planned'],
            textposition='inside',          # inside to avoid clash with threshold line
            textfont=dict(color='white')
        ))
        fig4.add_trace(go.Bar(
            name='Passed ✓', x=uat['cycle'], y=uat['passed'],
            marker_color='#22c55e',
            text=uat['passed'],
            textposition='outside'
        ))
        fig4.add_trace(go.Bar(
            name='Failed ✗', x=uat['cycle'], y=uat['failed'],
            marker_color='#ef4444',
            text=uat['failed'],
            textposition='outside'
        ))
        fig4.add_hline(y=19, line_dash="dot", line_color="#ef4444",
                       annotation_text="95% pass threshold (19/20)",
                       annotation_position="bottom right",
                       annotation_font_color="#ef4444",
                       annotation_font_size=11)
        fig4.update_layout(
            height=300, barmode='group',
            margin=dict(l=0,r=0,t=5,b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, title=''),
            yaxis=dict(gridcolor='rgba(128,128,128,0.1)', title='Test Cases',
                       range=[0, 24]),   # extra headroom so labels don't clip
            legend=dict(orientation='h',y=1.1,title=None)
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.markdown("<p class='sec'>Workstream Completion by Owner</p>", unsafe_allow_html=True)
    ws_avg = tasks.groupby('workstream')['completion'].mean().reset_index()
    ws_avg.columns = ['workstream','avg_completion']
    ws_avg['avg_completion'] = ws_avg['avg_completion'].round(1)
    ws_avg = ws_avg.sort_values('avg_completion', ascending=True)
    fig5 = px.bar(ws_avg, x='avg_completion', y='workstream', orientation='h',
                  color='avg_completion',
                  color_continuous_scale=['#ef4444','#f97316','#22c55e'],
                  range_color=[40,100],
                  text=ws_avg['avg_completion'].apply(lambda x: f"{x}%"))
    fig5.update_traces(textposition='outside')
    fig5.update_layout(
        height=280, margin=dict(l=0,r=70,t=5,b=0),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        coloraxis_showscale=False,
        xaxis=dict(title='Avg % Completion', range=[0,120], showgrid=False),
        yaxis=dict(title='')
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("---")
    st.markdown("<p class='sec'>Lessons Learned</p>", unsafe_allow_html=True)
    lessons = [
        ("Visibility over execution speed",
         "The KPI dashboard revealed cross-functional delays invisible in weekly status meetings. Early visibility enabled faster escalation and intervention before issues compounded."),
        ("Cross-functional dependencies = biggest risk",
         "A 2-day hardware delivery slip cascaded into manufacturing installation, pipeline integration, and UAT. Dependency chains must be actively managed — not just documented in a RAID log."),
        ("Early testing prevents late-stage failure",
         "UAT defects found in Cycle 1 could have been surfaced earlier with integration testing checkpoints in Phase 3. Shift-left testing must be planned at program inception."),
        ("Data-driven go/no-go decisions",
         "Quantified KPIs — 85% UAT pass rate vs 95% threshold — enabled an objective, defensible launch readiness assessment rather than opinion-based go/no-go calls."),
        ("Risk mitigation must be proactive",
         "5 of 8 RAID items were reactive responses to materialised issues. Risk triggers and escalation thresholds should be defined in Phase 1 and monitored throughout execution."),
    ]
    l1, l2 = st.columns(2)
    for i, (title, desc) in enumerate(lessons):
        col = l1 if i % 2 == 0 else l2
        with col:
            st.markdown(f"""
            <div style='padding:0.85rem 1rem;background:{tbg};border-left:2px solid {tc};
                 border-radius:0 6px 6px 0;margin-bottom:8px'>
              <div style='font-size:13px;font-weight:600;color:#fff;margin-bottom:4px'>{title}</div>
              <div style='font-size:12px;color:rgba(255,255,255,0.5);line-height:1.65'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ══════ TAB 2: TASK REGISTER ══════
with tab2:
    st.markdown(f"<p class='sec'>Task Register — {len(filtered)} of {len(tasks)} tasks shown · Filters in sidebar</p>", unsafe_allow_html=True)

    def cs(v):
        return {'Complete':'background-color:rgba(34,197,94,0.15);color:#16a34a',
                'At Risk':'background-color:rgba(239,68,68,0.15);color:#dc2626',
                'Delayed':'background-color:rgba(249,115,22,0.15);color:#ea580c',
                'In Progress':'background-color:rgba(59,130,246,0.15);color:#2563eb',
                'Not Started':'background-color:rgba(107,114,128,0.1);color:#6b7280'}.get(v,'')
    def cr(v):
        return {'High':'background-color:rgba(239,68,68,0.15);color:#dc2626',
                'Medium':'background-color:rgba(249,115,22,0.1);color:#ea580c',
                'Low':'background-color:rgba(34,197,94,0.1);color:#16a34a'}.get(v,'')

    disp = filtered[['task','phase','owner','workstream','status','completion','risk','start','end','duration','note']].copy()
    disp.columns = ['Task','Phase','Owner','Workstream','Status','% Done','Risk','Start','End','Duration','Notes']
    st.dataframe(
        disp.style.map(cs, subset=['Status']).map(cr, subset=['Risk']),
        use_container_width=True, height=520
    )

# ══════ TAB 3: RAID LOG ══════
with tab3:
    st.markdown("<p class='sec'>RAID Log — Risks · Assumptions · Issues · Dependencies</p>", unsafe_allow_html=True)
    rc1,rc2,rc3,rc4 = st.columns(4)
    for col, rtype, color in [
        (rc1,"Risk","#ef4444"),(rc2,"Issue","#f97316"),
        (rc3,"Assumption","#22c55e"),(rc4,"Dependency","#3b82f6")
    ]:
        n = len(raid[raid['type']==rtype])
        col.markdown(f"""
        <div style='background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);
             border-left:3px solid {color};border-radius:0 6px 6px 0;padding:0.75rem 1rem'>
          <div style='font-size:0.65rem;color:rgba(255,255,255,0.4);text-transform:uppercase;
               letter-spacing:0.08em'>{rtype}</div>
          <div style='font-size:1.5rem;font-weight:700;color:{color}'>{n}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    def ct(v):
        return {'Risk':'background-color:rgba(239,68,68,0.1);color:#dc2626',
                'Issue':'background-color:rgba(249,115,22,0.1);color:#ea580c',
                'Dependency':'background-color:rgba(59,130,246,0.1);color:#2563eb',
                'Assumption':'background-color:rgba(34,197,94,0.1);color:#16a34a'}.get(v,'')
    def ci(v):
        return {'High':'background-color:rgba(239,68,68,0.15);color:#dc2626',
                'Medium':'background-color:rgba(249,115,22,0.1);color:#ea580c'}.get(v,'')

    disp_raid = raid.copy()
    disp_raid.columns = ['Type','Description','Impact','Owner','Action','Status']
    st.dataframe(
        disp_raid.style.map(ct, subset=['Type']).map(ci, subset=['Impact']),
        use_container_width=True, height=380
    )

# ══════ TAB 4: RISK REGISTER ══════
with tab4:
    st.markdown("<p class='sec'>Risk Register — Probability × Impact Matrix</p>", unsafe_allow_html=True)
    r4a, r4b = st.columns(2)

    with r4a:
        st.markdown("**Risk Bubble Chart (P × I = Score)**")
        fig_risk = px.scatter(
            risk_register, x='probability', y='impact',
            size='score', color='score', text='id',
            color_continuous_scale=['#22c55e','#f97316','#ef4444'],
            range_color=[0,25], size_max=45,
            hover_data={'risk':True,'score':True,'owner':True,'mitigation':True}
        )
        fig_risk.update_traces(
            textposition='top center', textfont=dict(size=10),
            hovertemplate="<b>%{text}</b><br>%{customdata[0]}<br>Score: %{customdata[1]}<br>Owner: %{customdata[2]}<extra></extra>"
        )
        fig_risk.add_shape(type='rect', x0=3.5, x1=5.5, y0=3.5, y1=5.5,
                           fillcolor='rgba(239,68,68,0.08)',
                           line=dict(color='rgba(239,68,68,0.3)',dash='dot'))
        fig_risk.add_annotation(x=4.5, y=5.3, text="⚠ High Risk Zone",
                                showarrow=False, font=dict(color='#ef4444',size=11))
        fig_risk.update_layout(
            height=380, margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Probability (1–5)', range=[0,6], showgrid=False,
                       tickvals=[1,2,3,4,5]),
            yaxis=dict(title='Impact (1–5)', range=[0,6],
                       gridcolor='rgba(128,128,128,0.1)', tickvals=[1,2,3,4,5]),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with r4b:
        st.markdown("**Risk Register Detail**")
        def sc_col(v):
            if v >= 20: return 'background-color:rgba(239,68,68,0.2);color:#dc2626;font-weight:700'
            elif v >= 10: return 'background-color:rgba(249,115,22,0.15);color:#ea580c'
            return 'background-color:rgba(34,197,94,0.1);color:#16a34a'

        rr_disp = risk_register[['id','risk','probability','impact','score','owner','status']].copy()
        rr_disp.columns = ['ID','Risk','Prob','Impact','Score','Owner','Status']
        st.dataframe(
            rr_disp.style.map(sc_col, subset=['Score']),
            use_container_width=True, height=380
        )

    st.markdown("---")
    st.markdown("**Mitigation Actions**")
    for _, row in risk_register.iterrows():
        sc = '#ef4444' if row['score']>=20 else '#f97316' if row['score']>=10 else '#22c55e'
        st.markdown(f"""
        <div style='display:flex;gap:1rem;padding:0.7rem 0;
             border-bottom:1px solid rgba(255,255,255,0.06);align-items:flex-start'>
          <span style='font-family:monospace;font-size:0.72rem;color:{sc};
               background:rgba(255,255,255,0.05);padding:2px 8px;border-radius:3px;
               flex-shrink:0;margin-top:2px'>{row['id']} · {row['score']}</span>
          <div>
            <div style='font-size:13px;font-weight:500;color:#fff;margin-bottom:2px'>{row['risk']}</div>
            <div style='font-size:11px;color:rgba(255,255,255,0.45)'>{row['mitigation']} — <em>{row['owner']}</em></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════ TAB 5: CHANGE CONTROL ══════
with tab5:
    st.markdown("<p class='sec'>Change Request Log — 7 CRs · 6 Approved · 1 Rejected</p>", unsafe_allow_html=True)
    ca, cb, cc = st.columns(3)
    ca.metric("Total Change Requests", len(change_log))
    cb.metric("Approved", len(change_log[change_log['decision']=='Approved']), "changes incorporated")
    cc.metric("Rejected", len(change_log[change_log['decision']=='Rejected']), delta="scope protected", delta_color="off")

    st.markdown("<br>", unsafe_allow_html=True)
    def cd(v):
        return {'Approved':'background-color:rgba(34,197,94,0.15);color:#16a34a',
                'Rejected':'background-color:rgba(239,68,68,0.15);color:#dc2626'}.get(v,'')
    def ci2(v):
        return {'High':'background-color:rgba(239,68,68,0.12);color:#dc2626',
                'Medium':'background-color:rgba(249,115,22,0.1);color:#ea580c',
                'Low':'background-color:rgba(34,197,94,0.08);color:#16a34a'}.get(v,'')

    cl_disp = change_log[['id','request','impact','decision','owner','rationale']].copy()
    cl_disp.columns = ['CR ID','Change Request','Impact','Decision','Owner','Rationale']
    st.dataframe(
        cl_disp.style.map(cd, subset=['Decision']).map(ci2, subset=['Impact']),
        use_container_width=True, height=320
    )
    st.markdown("---")
    st.markdown(f"""
    <div class='alert-box'>
      <div class='alert-title' style='font-size:0.88rem;'>CR-C6 Rejection — Scope Protection Decision</div>
      <div class='alert-sub'>The request to reduce non-critical features was rejected to protect MVP integrity. This demonstrates formal change control discipline — not every request should be approved. The PM's role includes protecting project scope from unnecessary descoping under schedule pressure.</div>
    </div>
    """, unsafe_allow_html=True)

# ══════ TAB 6: STAKEHOLDERS ══════
with tab6:
    st.markdown("<p class='sec'>Stakeholder Register — Interest × Influence Matrix</p>", unsafe_allow_html=True)
    s1, s2 = st.columns([1,1])

    with s1:
        st.markdown("**Stakeholder Mapping**")
        eng_colors = {"Active":"#22c55e","Monitor":"#f97316","Inform":"#3b82f6"}
        fig_sh = px.scatter(
            stakeholders, x='int_j', y='inf_j',
            text='stakeholder', color='engagement',
            color_discrete_map=eng_colors,
            hover_data={'role':True,'engagement':True,
                        'int_j':False,'inf_j':False}
        )
        fig_sh.update_traces(
            marker=dict(size=22, opacity=0.9),
            textposition='top center',
            textfont=dict(size=10),
            hovertemplate="<b>%{text}</b><br>Role: %{customdata[0]}<br>Engagement: %{customdata[1]}<extra></extra>"
        )
        # Quadrant lines
        fig_sh.add_hline(y=2, line_dash="dot", line_color="rgba(255,255,255,0.15)")
        fig_sh.add_vline(x=2, line_dash="dot", line_color="rgba(255,255,255,0.15)")
        fig_sh.update_layout(
            height=380, margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title='Interest Level', tickvals=[1,2,3],
                       ticktext=['Low','Medium','High'],
                       showgrid=False, range=[0.5,3.8]),
            yaxis=dict(title='Influence Level', tickvals=[1,2,3],
                       ticktext=['Low','Medium','High'],
                       gridcolor='rgba(128,128,128,0.1)', range=[0.5,3.8]),
            legend=dict(title='Engagement', orientation='h', y=1.1)
        )
        st.plotly_chart(fig_sh, use_container_width=True)

    with s2:
        st.markdown("**Stakeholder Register**")
        def ceng(v):
            return {'Active':'background-color:rgba(34,197,94,0.15);color:#16a34a',
                    'Monitor':'background-color:rgba(249,115,22,0.1);color:#ea580c',
                    'Inform':'background-color:rgba(59,130,246,0.1);color:#2563eb'}.get(v,'')
        sh_disp = stakeholders[['stakeholder','role','interest','influence','engagement']].copy()
        sh_disp['interest'] = sh_disp['interest'].map({1:'Low',2:'Medium',3:'High'})
        sh_disp['influence'] = sh_disp['influence'].map({1:'Low',2:'Medium',3:'High'})
        sh_disp.columns = ['Stakeholder','Role','Interest','Influence','Engagement']
        st.dataframe(
            sh_disp.style.map(ceng, subset=['Engagement']),
            use_container_width=True, height=280
        )

    st.markdown("---")
    st.markdown("<p class='sec'>Key Requirements</p>", unsafe_allow_html=True)
    req1, req2 = st.columns(2)
    with req1:
        st.markdown("**Functional Requirements**")
        for req in [
            ("FR-01","AI system detects defects with ≥ 95% accuracy"),
            ("FR-02","System integrates with existing manufacturing line"),
            ("FR-03","KPI dashboard tracks project health in real time"),
            ("FR-04","UAT covers all defect classification scenarios"),
        ]:
            st.markdown(f"""
            <div style='display:flex;gap:10px;padding:7px 0;
                 border-bottom:1px solid rgba(255,255,255,0.06)'>
              <span style='font-family:monospace;font-size:0.7rem;color:{tc};flex-shrink:0'>{req[0]}</span>
              <span style='font-size:0.83rem;color:rgba(255,255,255,0.6)'>{req[1]}</span>
            </div>
            """, unsafe_allow_html=True)
    with req2:
        st.markdown("**Non-Functional Requirements**")
        for req in [
            ("NF-01","System reliability ≥ 99% uptime"),
            ("NF-02","Response time < 2 seconds per inspection"),
            ("NF-03","Scalable architecture for full production volume"),
            ("NF-04","Secure data pipeline with audit logging"),
        ]:
            st.markdown(f"""
            <div style='display:flex;gap:10px;padding:7px 0;
                 border-bottom:1px solid rgba(255,255,255,0.06)'>
              <span style='font-family:monospace;font-size:0.7rem;color:{tc};flex-shrink:0'>{req[0]}</span>
              <span style='font-size:0.83rem;color:rgba(255,255,255,0.6)'>{req[1]}</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
<p style='font-size:0.72rem;opacity:0.3;'>
Akshada Karade &nbsp;·&nbsp; MS Engineering Management, UMass Amherst &nbsp;·&nbsp;
Technical PM Case Study &nbsp;·&nbsp;
Tools: Smartsheet · Notion · Python · Streamlit · Plotly
</p>
""", unsafe_allow_html=True)
