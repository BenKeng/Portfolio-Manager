"""
Generate all Criterion B design diagrams for the IB CS IA.
Outputs PNG images into a /diagrams folder.
Run: python generate_diagrams.py
"""
import graphviz
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

OUT = "diagrams"
os.makedirs(OUT, exist_ok=True)

# ============================================================
# 1. SYSTEM FLOWCHART — Main Application Flow
# ============================================================
def flowchart():
    g = graphviz.Digraph("flowchart", format="png")
    g.attr(rankdir="TB", size="10,16", dpi="150", bgcolor="white")
    g.attr("node", fontname="Helvetica", fontsize="11")

    # Shapes: box=process, diamond=decision, parallelogram=IO, oval=terminal
    def terminal(name, label):
        g.node(name, label, shape="ellipse", style="filled", fillcolor="#D5E8D4", color="#82B366")
    def process(name, label):
        g.node(name, label, shape="box", style="filled,rounded", fillcolor="#DAE8FC", color="#6C8EBF")
    def decision(name, label):
        g.node(name, label, shape="diamond", style="filled", fillcolor="#FFF2CC", color="#D6B656")
    def io_node(name, label):
        g.node(name, label, shape="parallelogram", style="filled", fillcolor="#F8CECC", color="#B85450")

    terminal("start", "Start Application")
    process("init_session", "Initialize Session State\n(logged_in = False, table = None)")
    decision("auth_check", "User\nauthenticated?")
    io_node("show_login", "Display Login Form\n(Password Input)")
    io_node("input_pwd", "User Enters Password")
    decision("pwd_valid", "Password\ncorrect?")
    process("set_auth", "Set session_state\n[logged_in] = True")
    process("show_error", "Display\n'Access Denied'")
    process("show_dash", "Display Dashboard\nTitle & Welcome")
    decision("toggle_check", "Manual Entry\ntoggle ON?")
    io_node("show_editor", "Display Data Editor\n(Ticker, Date, Quantity)")
    io_node("show_upload", "Display CSV\nFile Uploader")
    decision("update_click", "Update button\nclicked?")
    decision("file_uploaded", "File\nuploaded?")
    process("validate", "Validate Ticker Symbols\nvia Yahoo Finance API")
    decision("valid_ticker", "All tickers\nvalid?")
    process("show_invalid", "Display Error:\nInvalid Tickers")
    process("csv_temp", "Write data to\nTemporary CSV")
    process("call_analytics", "Call load_data2()\n→ build_portfolio_from_csv()\n→ Portfolio.refresh_all()")
    process("store_table", "Store result DataFrame\nin session_state")
    process("display_table", "Display Performance\nInventory Table")
    process("calc_totals", "Calculate Aggregates\n(Total Profit, Cost, Return %)")
    process("show_metrics", "Display Metric Cards\n(P/L, Capital, Growth)")
    process("show_charts", "Render Charts\n(Line, Comparison, Pie)")
    io_node("download", "Download CSV\nExport Button")
    terminal("end", "End / Await\nUser Interaction")

    g.edge("start", "init_session")
    g.edge("init_session", "auth_check")
    g.edge("auth_check", "show_dash", label="Yes")
    g.edge("auth_check", "show_login", label="No")
    g.edge("show_login", "input_pwd")
    g.edge("input_pwd", "pwd_valid")
    g.edge("pwd_valid", "set_auth", label="Yes")
    g.edge("pwd_valid", "show_error", label="No")
    g.edge("show_error", "show_login")
    g.edge("set_auth", "show_dash")
    g.edge("show_dash", "toggle_check")
    g.edge("toggle_check", "show_editor", label="Yes")
    g.edge("toggle_check", "show_upload", label="No")
    g.edge("show_editor", "update_click")
    g.edge("update_click", "validate", label="Yes")
    g.edge("update_click", "end", label="No")
    g.edge("validate", "valid_ticker")
    g.edge("valid_ticker", "csv_temp", label="Yes")
    g.edge("valid_ticker", "show_invalid", label="No")
    g.edge("show_invalid", "show_editor")
    g.edge("show_upload", "file_uploaded")
    g.edge("file_uploaded", "csv_temp", label="Yes")
    g.edge("file_uploaded", "end", label="No")
    g.edge("csv_temp", "call_analytics")
    g.edge("call_analytics", "store_table")
    g.edge("store_table", "display_table")
    g.edge("display_table", "calc_totals")
    g.edge("calc_totals", "show_metrics")
    g.edge("show_metrics", "show_charts")
    g.edge("show_charts", "download")
    g.edge("download", "end")

    g.render(os.path.join(OUT, "1_system_flowchart"), cleanup=True)
    print("✓ System flowchart")


# ============================================================
# 2. DFD CONTEXT DIAGRAM (Level 0)
# ============================================================
def dfd_context():
    g = graphviz.Digraph("dfd_context", format="png")
    g.attr(rankdir="LR", size="12,6", dpi="150", bgcolor="white")
    g.attr("node", fontname="Helvetica", fontsize="12")

    # External entities = rectangles
    g.node("user", "User\n(Client)", shape="box", style="filled", fillcolor="#F8CECC", color="#B85450")
    g.node("yahoo", "Yahoo Finance\nAPI (yfinance)", shape="box", style="filled", fillcolor="#F8CECC", color="#B85450")
    g.node("filesystem", "Local\nFile System", shape="box", style="filled", fillcolor="#F8CECC", color="#B85450")

    # System = circle
    g.node("system", "Portfolio\nManager\nSystem", shape="circle", style="filled", fillcolor="#DAE8FC", color="#6C8EBF",
           width="2", height="2", fixedsize="true")

    g.edge("user", "system", label="  Password, Stock Data\n  (Ticker, Date, Qty)\n  CSV File Upload  ")
    g.edge("system", "user", label="  Dashboard, Charts,\n  Metrics, CSV Export,\n  Error Messages  ")
    g.edge("system", "yahoo", label="  API Request\n  (Ticker Symbol)  ")
    g.edge("yahoo", "system", label="  Historical Prices,\n  Current Prices  ")
    g.edge("system", "filesystem", label="  Save positions.csv  ")
    g.edge("filesystem", "system", label="  Read positions.csv  ")

    g.render(os.path.join(OUT, "2_dfd_context"), cleanup=True)
    print("✓ DFD Context Diagram")


# ============================================================
# 3. DFD LEVEL 1 — Internal Processes
# ============================================================
def dfd_level1():
    g = graphviz.Digraph("dfd_level1", format="png")
    g.attr(rankdir="TB", size="14,10", dpi="150", bgcolor="white")
    g.attr("node", fontname="Helvetica", fontsize="11")

    # External entities
    g.node("user", "User", shape="box", style="filled", fillcolor="#F8CECC", color="#B85450")
    g.node("yahoo", "Yahoo Finance API", shape="box", style="filled", fillcolor="#F8CECC", color="#B85450")
    g.node("disk", "File System", shape="box", style="filled", fillcolor="#F8CECC", color="#B85450")

    # Processes (circles)
    def proc(name, label):
        g.node(name, label, shape="circle", style="filled", fillcolor="#DAE8FC", color="#6C8EBF",
               width="1.5", height="1.5", fixedsize="true")

    proc("p1", "1.0\nAuthenticate\nUser")
    proc("p2", "2.0\nValidate\nInput")
    proc("p3", "3.0\nFetch Stock\nPrices")
    proc("p4", "4.0\nCompute\nAnalytics")
    proc("p5", "5.0\nGenerate\nVisualizations")
    proc("p6", "6.0\nExport\nData")

    # Data stores
    g.node("ds1", "D1 | Session State", shape="box", style="filled", fillcolor="#FFF2CC", color="#D6B656")
    g.node("ds2", "D2 | Portfolio DataFrame", shape="box", style="filled", fillcolor="#FFF2CC", color="#D6B656")

    g.edge("user", "p1", label="Password")
    g.edge("p1", "ds1", label="Auth status")
    g.edge("user", "p2", label="Ticker, Date,\nQty / CSV")
    g.edge("p2", "p3", label="Validated\npositions")
    g.edge("p3", "yahoo", label="API request\n(ticker)")
    g.edge("yahoo", "p3", label="Price data")
    g.edge("p3", "p4", label="Raw prices\n+ quantities")
    g.edge("p4", "ds2", label="Results\nDataFrame")
    g.edge("ds2", "p5", label="Table data")
    g.edge("p5", "user", label="Charts,\nMetrics")
    g.edge("ds2", "p6", label="Table data")
    g.edge("p6", "user", label="CSV download")
    g.edge("p6", "disk", label="Save CSV")

    g.render(os.path.join(OUT, "3_dfd_level1"), cleanup=True)
    print("✓ DFD Level 1")


# ============================================================
# 4. UML CLASS DIAGRAM
# ============================================================
def uml_class():
    g = graphviz.Digraph("uml_class", format="png")
    g.attr(rankdir="TB", size="12,8", dpi="150", bgcolor="white")
    g.attr("node", fontname="Courier", fontsize="10")

    stock_label = """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" BGCOLOR="white">
    <TR><TD BGCOLOR="#DAE8FC" COLSPAN="2"><B>StockPosition</B></TD></TR>
    <TR><TD ALIGN="LEFT">- ticker : str</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">- purchase_date : datetime</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">- quantity : int</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">- current_value : float</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">- buy_value : float</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">- profit : float</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">- return_pct : float</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">- cost_per_share : float</TD><TD></TD></TR>
    <TR><TD BGCOLOR="#E8E8E8" COLSPAN="2"></TD></TR>
    <TR><TD ALIGN="LEFT">+ __init__(ticker, date, qty)</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">+ update_metrics() : void</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">+ to_dict() : dict</TD><TD></TD></TR>
    </TABLE>>"""

    port_label = """<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="6" BGCOLOR="white">
    <TR><TD BGCOLOR="#D5E8D4" COLSPAN="2"><B>Portfolio</B></TD></TR>
    <TR><TD ALIGN="LEFT">- positions : list[StockPosition]</TD><TD></TD></TR>
    <TR><TD BGCOLOR="#E8E8E8" COLSPAN="2"></TD></TR>
    <TR><TD ALIGN="LEFT">+ __init__()</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">+ add_position(ticker, date, qty) : void</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">+ refresh_all() : void</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">+ get_summary_df() : DataFrame</TD><TD></TD></TR>
    <TR><TD ALIGN="LEFT">+ get_totals() : tuple</TD><TD></TD></TR>
    </TABLE>>"""

    g.node("StockPosition", stock_label, shape="none")
    g.node("Portfolio", port_label, shape="none")

    g.edge("Portfolio", "StockPosition", label="  1..*  ", arrowhead="diamond",
           style="bold", dir="both", arrowtail="odiamond")

    g.render(os.path.join(OUT, "4_uml_class_diagram"), cleanup=True)
    print("✓ UML Class Diagram")


# ============================================================
# 5. MODULE DEPENDENCY DIAGRAM
# ============================================================
def module_dependency():
    g = graphviz.Digraph("module_deps", format="png")
    g.attr(rankdir="TB", size="10,8", dpi="150", bgcolor="white")
    g.attr("node", fontname="Helvetica", fontsize="12", shape="box3d", style="filled")

    g.node("app", "App.py\n(View Layer)", fillcolor="#DAE8FC", color="#6C8EBF")
    g.node("analytics", "analytics.py\n(Controller)", fillcolor="#D5E8D4", color="#82B366")
    g.node("models", "models.py\n(Model / OOP)", fillcolor="#FFF2CC", color="#D6B656")
    g.node("data_loader", "data_loader.py\n(Data Access / API)", fillcolor="#F8CECC", color="#B85450")
    g.node("plotting", "plotting.py\n(Visualization)", fillcolor="#E1D5E7", color="#9673A6")

    g.node("streamlit", "Streamlit\n(Framework)", shape="box", fillcolor="#EEEEEE", color="#999999")
    g.node("yfinance", "yfinance\n(REST API)", shape="box", fillcolor="#EEEEEE", color="#999999")
    g.node("pandas", "pandas\n(DataFrames)", shape="box", fillcolor="#EEEEEE", color="#999999")
    g.node("matplotlib", "matplotlib\n(Charts)", shape="box", fillcolor="#EEEEEE", color="#999999")

    g.edge("app", "analytics", label="load_data2()")
    g.edge("app", "plotting", label="price_history_figure()\nmulti_stock_history_figure()")
    g.edge("app", "data_loader", label="is_valid_ticker()")
    g.edge("analytics", "models", label="build_portfolio_from_csv()")
    g.edge("models", "data_loader", label="fetch_stock_value()")
    g.edge("data_loader", "yfinance", style="dashed")
    g.edge("app", "streamlit", style="dashed")
    g.edge("plotting", "matplotlib", style="dashed")
    g.edge("plotting", "yfinance", style="dashed")
    g.edge("models", "pandas", style="dashed")
    g.edge("analytics", "pandas", style="dashed")

    g.render(os.path.join(OUT, "5_module_dependency"), cleanup=True)
    print("✓ Module Dependency Diagram")


# ============================================================
# 6. ANNOTATED UI MOCKUPS (matplotlib)
# ============================================================
def ui_mockups():
    # --- LOGIN SCREEN ---
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Browser frame
    ax.add_patch(FancyBboxPatch((0.5, 0.3), 9, 6.2, boxstyle="round,pad=0.1",
                                facecolor="#F7F7F7", edgecolor="#333333", linewidth=2))
    ax.text(5, 6.0, "Login", fontsize=20, ha="center", fontweight="bold")

    # Password field
    ax.add_patch(FancyBboxPatch((2.5, 3.8), 5, 0.7, boxstyle="round,pad=0.05",
                                facecolor="white", edgecolor="#CCCCCC"))
    ax.text(5, 4.15, "••••••••", fontsize=14, ha="center", color="#999999")
    ax.text(2.5, 4.7, "Password", fontsize=11, ha="left", color="#555555")

    # Login button
    ax.add_patch(FancyBboxPatch((3.5, 2.5), 3, 0.7, boxstyle="round,pad=0.1",
                                facecolor="#FF4B4B", edgecolor="#CC3333"))
    ax.text(5, 2.85, "Login", fontsize=14, ha="center", color="white", fontweight="bold")

    # Annotations
    ax.annotate("Password input field\n(type='password', masked)", xy=(7.5, 4.15), xytext=(8.5, 5.5),
                fontsize=9, ha="center", arrowprops=dict(arrowstyle="->", color="#B85450"),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF2CC", edgecolor="#D6B656"))
    ax.annotate("st.button() triggers\nauthentication check\nagainst st.secrets", xy=(6.5, 2.85), xytext=(8.5, 1.5),
                fontsize=9, ha="center", arrowprops=dict(arrowstyle="->", color="#B85450"),
                bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF2CC", edgecolor="#D6B656"))

    fig.savefig(os.path.join(OUT, "6a_mockup_login.png"), dpi=150, bbox_inches="tight")
    plt.close()

    # --- DASHBOARD SCREEN ---
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 11)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    # Main frame
    ax.add_patch(FancyBboxPatch((0.3, 0.3), 13.4, 10.4, boxstyle="round,pad=0.1",
                                facecolor="#F7F7F7", edgecolor="#333333", linewidth=2))

    # Title
    ax.text(7, 10.2, "Investment Portfolio Analytics", fontsize=18, ha="center", fontweight="bold")

    # Toggle
    ax.add_patch(FancyBboxPatch((1, 9.3), 4, 0.5, boxstyle="round,pad=0.05",
                                facecolor="#D5E8D4", edgecolor="#82B366"))
    ax.text(3, 9.55, "☑ Enable Manual Table Entry", fontsize=9, ha="center")

    # Data editor table
    ax.add_patch(FancyBboxPatch((1, 7.3), 12, 1.8, boxstyle="round,pad=0.05",
                                facecolor="white", edgecolor="#CCCCCC"))
    ax.text(7, 8.8, "Ticker Symbol    |    Acquisition Date    |    Shares Owned", 
            fontsize=10, ha="center", fontfamily="monospace", fontweight="bold")
    ax.text(7, 8.3, "AAPL                    2025-01-15                    10", fontsize=10, ha="center", fontfamily="monospace")
    ax.text(7, 7.8, "TSLA                     2025-06-01                     5", fontsize=10, ha="center", fontfamily="monospace")

    # Buttons
    ax.add_patch(FancyBboxPatch((1, 6.5), 3.5, 0.5, boxstyle="round,pad=0.1",
                                facecolor="#FF4B4B", edgecolor="#CC3333"))
    ax.text(2.75, 6.75, "Update Portfolio View", fontsize=9, ha="center", color="white", fontweight="bold")
    ax.add_patch(FancyBboxPatch((5, 6.5), 3.5, 0.5, boxstyle="round,pad=0.1",
                                facecolor="#FF4B4B", edgecolor="#CC3333"))
    ax.text(6.75, 6.75, "Save Entry to Local Disk", fontsize=9, ha="center", color="white", fontweight="bold")

    # Metric cards
    for i, (label, val) in enumerate([("Unrealized P/L", "$1,240.50"), ("Total Capital", "$12,500.00"), ("Growth", "9.92%")]):
        x = 1 + i * 4.2
        ax.add_patch(FancyBboxPatch((x, 5.2), 3.8, 1.0, boxstyle="round,pad=0.1",
                                    facecolor="#DAE8FC", edgecolor="#6C8EBF"))
        ax.text(x + 1.9, 5.9, label, fontsize=9, ha="center", color="#555555")
        ax.text(x + 1.9, 5.5, val, fontsize=12, ha="center", fontweight="bold")

    # Chart area
    ax.add_patch(FancyBboxPatch((1, 1.5), 8, 3.4, boxstyle="round,pad=0.05",
                                facecolor="white", edgecolor="#CCCCCC"))
    ax.text(5, 4.5, "[ Asset History | Comparison View | Capital Allocation ]",
            fontsize=9, ha="center", fontweight="bold", color="#6C8EBF")
    ax.text(5, 3.2, "Stock Price Line Chart\nwith Buy Date Marker", fontsize=11, ha="center", color="#777777")

    # Pie area
    ax.add_patch(FancyBboxPatch((9.5, 1.5), 3.5, 3.4, boxstyle="round,pad=0.05",
                                facecolor="white", edgecolor="#CCCCCC"))
    ax.text(11.25, 3.5, "Pie Chart\n(Allocation\nby Cost)", fontsize=11, ha="center", color="#777777")

    # Download button
    ax.add_patch(FancyBboxPatch((1, 0.6), 4, 0.5, boxstyle="round,pad=0.1",
                                facecolor="#262730", edgecolor="#111111"))
    ax.text(3, 0.85, "⬇ Export Portfolio Report (CSV)", fontsize=9, ha="center", color="white")

    # Annotations
    ax.annotate("st.data_editor with\ncalendar date picker\nand dynamic rows", xy=(13, 8.2), xytext=(13.5, 9.5),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="->", color="#B85450"),
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFF2CC", edgecolor="#D6B656"))
    ax.annotate("st.metric() cards\nwith delta indicator", xy=(7, 5.7), xytext=(13.2, 6.5),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="->", color="#B85450"),
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFF2CC", edgecolor="#D6B656"))
    ax.annotate("st.tabs() for\nchart navigation", xy=(5, 4.5), xytext=(0.5, 5.0),
                fontsize=8, ha="center", arrowprops=dict(arrowstyle="->", color="#B85450"),
                bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFF2CC", edgecolor="#D6B656"))

    fig.savefig(os.path.join(OUT, "6b_mockup_dashboard.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ UI Mockups")


# ============================================================
# 7. DATA DICTIONARY TABLE (matplotlib table)
# ============================================================
def data_dictionary():
    fig, axes = plt.subplots(2, 1, figsize=(12, 7))
    fig.patch.set_facecolor("white")

    # Input CSV
    ax = axes[0]
    ax.axis("off")
    ax.set_title("Input Data Structure — positions.csv", fontsize=13, fontweight="bold", pad=10, loc="left")
    cols = ["Field", "Data Type", "Description", "Example", "Validation"]
    rows = [
        ["ticker", "String", "Stock exchange symbol", "AAPL", "Checked via is_valid_ticker()"],
        ["datetime", "Date (YYYY-MM-DD)", "Purchase date of shares", "2025-01-15", "Parsed by pd.to_datetime()"],
        ["quantity", "Integer", "Number of shares owned", "10", "Must be ≥ 1, not NaN"],
    ]
    table1 = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="left")
    table1.auto_set_font_size(False)
    table1.set_fontsize(9)
    table1.scale(1, 1.6)
    for (row, col), cell in table1.get_celld().items():
        if row == 0:
            cell.set_facecolor("#DAE8FC")
            cell.set_text_props(fontweight="bold")
        cell.set_edgecolor("#CCCCCC")

    # Output DataFrame
    ax2 = axes[1]
    ax2.axis("off")
    ax2.set_title("Output Data Structure — Portfolio Summary DataFrame", fontsize=13, fontweight="bold", pad=10, loc="left")
    cols2 = ["Column", "Data Type", "Source", "Example"]
    rows2 = [
        ["Stock Ticker", "String", "User input (uppercased)", "AAPL"],
        ["Purchase Date", "Datetime", "User input (parsed)", "2025-01-15"],
        ["Quantity", "Integer", "User input", "10"],
        ["Cost Per Share ($)", "Float", "buy_value / quantity", "142.50"],
        ["Total Cost ($)", "Float", "buy_price × quantity", "1425.00"],
        ["Current Value ($)", "Float", "current_price × quantity", "1892.30"],
        ["Profit ($)", "Float", "current_value − buy_value", "467.30"],
        ["Percentage Return (%)", "Float", "(profit / buy_value) × 100", "32.79"],
    ]
    table2 = ax2.table(cellText=rows2, colLabels=cols2, loc="center", cellLoc="left")
    table2.auto_set_font_size(False)
    table2.set_fontsize(9)
    table2.scale(1, 1.5)
    for (row, col), cell in table2.get_celld().items():
        if row == 0:
            cell.set_facecolor("#D5E8D4")
            cell.set_text_props(fontweight="bold")
        cell.set_edgecolor("#CCCCCC")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "7_data_dictionary.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Data Dictionary")


# ============================================================
# 8. TEST PLAN TABLE
# ============================================================
def test_plan():
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    fig.patch.set_facecolor("white")
    ax.axis("off")
    ax.set_title("Test Plan — Aligned to Success Criteria", fontsize=14, fontweight="bold", pad=15, loc="left")

    cols = ["#", "What to Test", "Test Input", "Expected Result", "Type"]
    rows = [
        ["1", "Password authentication (correct)", "Password: 'admin'", "Dashboard loads successfully", "Normal"],
        ["2", "Password authentication (wrong)", "Password: 'wrongpwd'", "'Access Denied' error displayed", "Abnormal"],
        ["3", "Manual entry with valid data", "AAPL, 2025-01-15, 10", "Row appears with profit/cost metrics", "Normal"],
        ["4", "Invalid ticker symbol", "XYZFAKE, 2025-01-15, 5", "'Invalid Tickers Detected' error", "Abnormal"],
        ["5", "Empty table submission", "No rows, click Update", "'Enter at least one valid position' warning", "Boundary"],
        ["6", "CSV upload (correct format)", "positions.csv (3 rows)", "Dashboard populates with 3 stock rows", "Normal"],
        ["7", "CSV upload (wrong columns)", "CSV without 'ticker' column", "ValueError / error message shown", "Abnormal"],
        ["8", "Future purchase date", "AAPL, 2030-01-01, 5", "Handled gracefully (no crash)", "Extreme"],
        ["9", "Quantity of zero", "AAPL, 2025-01-15, 0", "Division by zero handled", "Boundary"],
        ["10", "Single stock chart renders", "Select AAPL from dropdown", "Line chart + red buy-date line appears", "Normal"],
        ["11", "Multi-stock comparison chart", "2+ stocks in portfolio", "All stocks plotted on one graph", "Normal"],
        ["12", "Pie chart allocation", "3 stocks with different costs", "Pie chart shows % breakdown", "Normal"],
        ["13", "CSV export download", "Click 'Export' button", "Browser downloads .csv file", "Normal"],
        ["14", "Save to local disk", "Click 'Save' button", "File saved to config/positions.csv", "Normal"],
        ["15", "Ticker with special chars", "Ticker: '!!!@#$'", "Invalid ticker error displayed", "Extreme"],
    ]

    table = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="left")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)

    type_colors = {"Normal": "#D5E8D4", "Abnormal": "#F8CECC", "Boundary": "#FFF2CC", "Extreme": "#E1D5E7"}
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#6C8EBF")
            cell.set_text_props(fontweight="bold", color="white")
        elif col == 4 and row > 0:
            val = rows[row - 1][4]
            cell.set_facecolor(type_colors.get(val, "white"))
        cell.set_edgecolor("#CCCCCC")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "8_test_plan.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Test Plan")


# ============================================================
# 9. DEVELOPMENT SCHEDULE
# ============================================================
def dev_schedule():
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    fig.patch.set_facecolor("white")
    ax.axis("off")
    ax.set_title("Development Schedule", fontsize=14, fontweight="bold", pad=15, loc="left")

    cols = ["Phase", "Week", "Tasks", "Deliverable"]
    rows = [
        ["Plan", "1", "Client interview 1; identify requirements;\nresearch technology options", "Scenario & rationale draft"],
        ["Plan", "2", "Client interview 2; finalize success criteria;\nclient sign-off", "Success criteria list"],
        ["Design", "3", "Create flowchart, DFD, UML class diagram;\ndesign UI mockups", "Design overview document"],
        ["Design", "4", "Write data dictionary; design test plan;\ncreate Record of Tasks", "Test plan & Record of Tasks"],
        ["Develop", "5–6", "Implement data_loader.py (API layer);\nimplement models.py (OOP classes)", "Working API + model layer"],
        ["Develop", "7–8", "Build analytics.py (controller);\nbuild App.py (Streamlit UI)", "Functional dashboard"],
        ["Develop", "9", "Implement plotting.py (charts);\nadd ticker validation, CSV export, save", "Complete feature set"],
        ["Test", "10", "Execute test plan; fix bugs;\ntest edge cases and error handling", "Test results documentation"],
        ["Implement", "11", "Deploy to Streamlit Cloud;\ntrain client; gather feedback", "Live deployed product"],
        ["Evaluate", "12", "Client feedback interview;\nwrite evaluation & recommendations", "Criterion E document"],
    ]

    table = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="left")
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2.2)

    phase_colors = {"Plan": "#DAE8FC", "Design": "#D5E8D4", "Develop": "#FFF2CC",
                    "Test": "#F8CECC", "Implement": "#E1D5E7", "Evaluate": "#FFE6CC"}
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_facecolor("#6C8EBF")
            cell.set_text_props(fontweight="bold", color="white")
        elif col == 0 and row > 0:
            val = rows[row - 1][0]
            cell.set_facecolor(phase_colors.get(val, "white"))
            cell.set_text_props(fontweight="bold")
        cell.set_edgecolor("#CCCCCC")

    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "9_development_schedule.png"), dpi=150, bbox_inches="tight")
    plt.close()
    print("✓ Development Schedule")


# ============================================================
# 10. PSEUDOCODE — update_metrics() algorithm
# ============================================================
def pseudocode_diagram():
    g = graphviz.Digraph("pseudocode_flow", format="png")
    g.attr(rankdir="TB", size="8,12", dpi="150", bgcolor="white")
    g.attr("node", fontname="Courier", fontsize="10")

    def terminal(n, l):
        g.node(n, l, shape="ellipse", style="filled", fillcolor="#D5E8D4", color="#82B366")
    def process(n, l):
        g.node(n, l, shape="box", style="filled,rounded", fillcolor="#DAE8FC", color="#6C8EBF")
    def decision(n, l):
        g.node(n, l, shape="diamond", style="filled", fillcolor="#FFF2CC", color="#D6B656")

    terminal("s", "update_metrics(self)")
    process("p1", "stock = yf.Ticker(self.ticker)")
    process("p2", "current_price =\nstock.history(period='1d')['Close'][-1]")
    decision("d1", "History\nempty?")
    process("p2b", "Return (0.0, 0.0)")
    process("p3", "hist = stock.history(period='max')\nhist.index.tz_localize(None)")
    process("p4", "buy_price =\nhist.loc[purchase_date:, 'Close'][0]")
    process("p5", "current_value =\ncurrent_price × quantity")
    process("p6", "buy_value =\nbuy_price × quantity")
    process("p7", "profit =\ncurrent_value − buy_value")
    decision("d2", "buy_value\n≠ 0?")
    process("p8a", "return_pct =\n(profit / buy_value) × 100")
    process("p8b", "return_pct = 0.0")
    process("p9", "cost_per_share =\nbuy_value / quantity")
    terminal("e", "End")

    g.edge("s", "p1")
    g.edge("p1", "p2")
    g.edge("p2", "d1")
    g.edge("d1", "p2b", label="Yes")
    g.edge("d1", "p3", label="No")
    g.edge("p3", "p4")
    g.edge("p4", "p5")
    g.edge("p5", "p6")
    g.edge("p6", "p7")
    g.edge("p7", "d2")
    g.edge("d2", "p8a", label="Yes")
    g.edge("d2", "p8b", label="No")
    g.edge("p8a", "p9")
    g.edge("p8b", "p9")
    g.edge("p9", "e")

    g.render(os.path.join(OUT, "10_pseudocode_flowchart"), cleanup=True)
    print("✓ Pseudocode Flowchart")


# ============================================================
# RUN ALL
# ============================================================
if __name__ == "__main__":
    print(f"Generating diagrams into ./{OUT}/\n")
    flowchart()
    dfd_context()
    dfd_level1()
    uml_class()
    module_dependency()
    ui_mockups()
    data_dictionary()
    test_plan()
    dev_schedule()
    pseudocode_diagram()
    print(f"\n✅ All diagrams saved to ./{OUT}/")
