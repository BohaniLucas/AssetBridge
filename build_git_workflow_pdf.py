"""
AssetBridge — Team Git Workflow & Collaboration Guide PDF Generator
Produces a production-ready, beautifully styled multi-page PDF document.
"""

import os
import sys

def build_pdf(filename="AssetBridge_Team_Git_Workflow_Guide.pdf"):
    # Standard A4 size in points
    PAGE_WIDTH = 595.28
    PAGE_HEIGHT = 841.89
    MARGIN_LEFT = 40.0
    CONTENT_WIDTH = PAGE_WIDTH - (MARGIN_LEFT * 2) # 515.28

    pages = []
    
    class PageCanvas:
        def __init__(self, page_num, total_pages=3):
            self.page_num = page_num
            self.total_pages = total_pages
            self.commands = []
            
        def add(self, cmd):
            self.commands.append(cmd)
            
        def set_fill_rgb(self, r, g, b):
            self.add(f"{r:.3f} {g:.3f} {b:.3f} rg")
            
        def set_stroke_rgb(self, r, g, b):
            self.add(f"{r:.3f} {g:.3f} {b:.3f} RG")
            
        def set_line_width(self, w):
            self.add(f"{w:.2f} w")
            
        def draw_rect(self, x, y, w, h, fill=True, stroke=False):
            op = "b" if (fill and stroke) else ("f" if fill else "s")
            self.add(f"{x:.2f} {y:.2f} {w:.2f} {h:.2f} re {op}")
            
        def draw_line(self, x1, y1, x2, y2):
            self.add(f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l s")
            
        def draw_text(self, text, x, y, font="F1", size=10, r=0.06, g=0.09, b=0.16):
            safe_text = (
                text.replace("\\", "\\\\")
                    .replace("(", "\\(")
                    .replace(")", "\\)")
            )
            self.set_fill_rgb(r, g, b)
            self.add(f"BT /{font} {size:.2f} Tf {x:.2f} {y:.2f} Td ({safe_text}) Tj ET")

        def draw_footer(self):
            # Thin footer divider
            self.set_stroke_rgb(0.85, 0.88, 0.92)
            self.set_line_width(0.75)
            self.draw_line(MARGIN_LEFT, 32, MARGIN_LEFT + CONTENT_WIDTH, 32)
            
            # Footer text
            self.draw_text("AssetBridge Engineering Guide • Confidential & Internal Team Use", MARGIN_LEFT, 20, "F1", 8, 0.45, 0.52, 0.62)
            page_str = f"Page {self.page_num} of {self.total_pages}"
            self.draw_text(page_str, MARGIN_LEFT + CONTENT_WIDTH - 55, 20, "F2", 8, 0.25, 0.35, 0.50)

    # =========================================================================
    # PAGE 1: Overview, Architecture & Initial Setup
    # =========================================================================
    p1 = PageCanvas(1, 3)
    
    # ── Top Hero Header Card ──
    p1.set_fill_rgb(0.06, 0.09, 0.16) # #0f172a Dark Navy
    p1.draw_rect(MARGIN_LEFT, 715, CONTENT_WIDTH, 96, fill=True, stroke=False)
    
    # Accent top-border strip (Cyan)
    p1.set_fill_rgb(0.00, 0.76, 1.00) # #00c2ff
    p1.draw_rect(MARGIN_LEFT, 807, CONTENT_WIDTH, 4, fill=True, stroke=False)
    
    # Header Badges
    p1.set_fill_rgb(0.12, 0.20, 0.35)
    p1.draw_rect(MARGIN_LEFT + 14, 786, 75, 14, fill=True)
    p1.draw_text("ASSETBRIDGE", MARGIN_LEFT + 19, 790, "F2", 7.5, 0.00, 0.76, 1.00)
    
    p1.set_fill_rgb(0.12, 0.20, 0.35)
    p1.draw_rect(MARGIN_LEFT + 95, 786, 115, 14, fill=True)
    p1.draw_text("TEAM WORKFLOW GUIDE", MARGIN_LEFT + 100, 790, "F2", 7.5, 1.0, 1.0, 1.0)
    
    p1.set_fill_rgb(0.12, 0.20, 0.35)
    p1.draw_rect(MARGIN_LEFT + 216, 786, 70, 14, fill=True)
    p1.draw_text("GIT & GITHUB", MARGIN_LEFT + 221, 790, "F2", 7.5, 0.57, 0.77, 1.0)
    
    # Main Header Titles
    p1.draw_text("Team Git Collaboration & Workflow Guide", MARGIN_LEFT + 14, 764, "F2", 15.5, 1.0, 1.0, 1.0)
    p1.draw_text("How to Work in Your Personal Branch, Sync with dev, and Push Cleanly", MARGIN_LEFT + 14, 748, "F1", 9.5, 0.58, 0.77, 0.99)
    p1.draw_text("Repository: https://github.com/BohaniLucas/AssetBridge.git", MARGIN_LEFT + 14, 727, "F3", 8.5, 0.22, 0.74, 0.97)

    # ── Section 1: Branch Structure & Roles ──
    y = 692
    p1.draw_text("1. Team Branch Structure & Roles", MARGIN_LEFT, y, "F2", 12.5, 0.06, 0.09, 0.16)
    p1.set_stroke_rgb(0.00, 0.76, 1.00)
    p1.set_line_width(1.5)
    p1.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    y -= 18
    p1.draw_text("Our project utilizes a 3-tier structure to isolate in-progress work and protect the demo codebase:", MARGIN_LEFT, y, "F1", 9, 0.30, 0.35, 0.45)

    # Table Header
    y -= 14
    p1.set_fill_rgb(0.12, 0.16, 0.23)
    p1.draw_rect(MARGIN_LEFT, y - 4, CONTENT_WIDTH, 17, fill=True)
    p1.draw_text("BRANCH", MARGIN_LEFT + 8, y, "F2", 8.5, 1.0, 1.0, 1.0)
    p1.draw_text("PURPOSE & ROLE", MARGIN_LEFT + 120, y, "F2", 8.5, 1.0, 1.0, 1.0)
    p1.draw_text("ASSIGNED TO", MARGIN_LEFT + 360, y, "F2", 8.5, 1.0, 1.0, 1.0)
    p1.draw_text("DIRECT PUSH?", MARGIN_LEFT + 445, y, "F2", 8.5, 1.0, 1.0, 1.0)

    # Table Rows
    rows = [
        ("main", "Production Release & Final Hackathon Submission", "Team Lead", "NEVER (Protected)", (1.0, 0.95, 0.95), (0.9, 0.2, 0.2)),
        ("dev", "Shared Integration / Staging branch (all features land here)", "Entire Team", "Via Merge / PR", (0.95, 0.98, 1.0), (0.1, 0.4, 0.8)),
        ("fullstack/Lucas", "Lucas's dedicated feature & full-stack development branch", "Lucas", "YES (Your branch)", (1.0, 1.0, 1.0), (0.1, 0.6, 0.3)),
        ("fullstack/Rory", "Rory's dedicated feature & full-stack development branch", "Rory", "YES (Your branch)", (0.97, 0.98, 0.99), (0.1, 0.6, 0.3)),
        ("fullstack/Dokotela", "Dokotela's dedicated feature & full-stack branch", "Dokotela", "YES (Your branch)", (1.0, 1.0, 1.0), (0.1, 0.6, 0.3)),
    ]

    for bname, role, who, can_push, bg_col, push_col in rows:
        y -= 17
        p1.set_fill_rgb(*bg_col)
        p1.draw_rect(MARGIN_LEFT, y - 3, CONTENT_WIDTH, 17, fill=True)
        p1.set_stroke_rgb(0.88, 0.90, 0.94)
        p1.set_line_width(0.5)
        p1.draw_line(MARGIN_LEFT, y - 3, MARGIN_LEFT + CONTENT_WIDTH, y - 3)

        p1.draw_text(bname, MARGIN_LEFT + 8, y + 1, "F4", 8.5, 0.12, 0.15, 0.22)
        p1.draw_text(role, MARGIN_LEFT + 120, y + 1, "F1", 8.5, 0.25, 0.30, 0.38)
        p1.draw_text(who, MARGIN_LEFT + 360, y + 1, "F2", 8.5, 0.15, 0.20, 0.28)
        p1.draw_text(can_push, MARGIN_LEFT + 445, y + 1, "F2", 8.0, *push_col)

    # ── Section 2: First-Time Setup & Onboarding ──
    y -= 26
    p1.draw_text("2. First-Time Setup & Branch Onboarding", MARGIN_LEFT, y, "F2", 12.5, 0.06, 0.09, 0.16)
    p1.set_stroke_rgb(0.00, 0.76, 1.00)
    p1.set_line_width(1.5)
    p1.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    y -= 16
    p1.draw_text("Run these steps once in PowerShell / Terminal when getting started on your laptop:", MARGIN_LEFT, y, "F1", 9, 0.30, 0.35, 0.45)

    y -= 10
    code_box_h = 138
    p1.set_fill_rgb(0.07, 0.10, 0.17)
    p1.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=True)
    p1.set_stroke_rgb(0.20, 0.25, 0.35)
    p1.set_line_width(1.0)
    p1.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=False, stroke=True)

    cy = y - 14
    commands_s2 = [
        ("# 1. Clone the project (if setting up fresh)", (0.58, 0.64, 0.72)),
        ("git clone https://github.com/BohaniLucas/AssetBridge.git", (0.22, 0.74, 0.97)),
        ("cd AssetBridge", (0.22, 0.74, 0.97)),
        ("", (1, 1, 1)),
        ("# 2. Fetch all branches created by team members on GitHub", (0.58, 0.64, 0.72)),
        ("git fetch origin", (0.22, 0.74, 0.97)),
        ("", (1, 1, 1)),
        ("# 3. Switch to YOUR designated branch (choose your name):", (0.58, 0.64, 0.72)),
        ("git checkout fullstack/Rory       # If you are Rory", (0.98, 0.80, 0.08)),
        ("git checkout fullstack/Dokotela   # If you are Dokotela", (0.98, 0.80, 0.08)),
        ("git checkout fullstack/Lucas      # If you are Lucas", (0.98, 0.80, 0.08)),
        ("", (1, 1, 1)),
        ("# 4. Confirm you are on your branch (asterisk * marks active branch)", (0.58, 0.64, 0.72)),
        ("git branch", (0.22, 0.74, 0.97)),
    ]

    for line, col in commands_s2:
        if line:
            font = "F4" if line.startswith("#") else "F3"
            p1.draw_text(line, MARGIN_LEFT + 12, cy, font, 8.5, *col)
        cy -= 9.5

    # ── Section 3: Daily Routine Preview ──
    y = cy - 24
    p1.set_fill_rgb(0.94, 0.97, 1.0)
    p1.draw_rect(MARGIN_LEFT, y - 56, CONTENT_WIDTH, 56, fill=True)
    p1.set_stroke_rgb(0.20, 0.50, 0.90)
    p1.set_line_width(1.0)
    p1.draw_rect(MARGIN_LEFT, y - 56, CONTENT_WIDTH, 56, fill=False, stroke=True)
    # Left accent bar
    p1.set_fill_rgb(0.14, 0.40, 0.90)
    p1.draw_rect(MARGIN_LEFT, y - 56, 4, 56, fill=True)

    p1.draw_text("KEY COLLABORATION PRINCIPLE: ALWAYS PULL BEFORE YOU WRITE", MARGIN_LEFT + 14, y - 16, "F2", 9.5, 0.10, 0.30, 0.75)
    p1.draw_text("To prevent merge conflicts, make it an absolute habit to sync dev into your branch each morning.", MARGIN_LEFT + 14, y - 29, "F1", 8.5, 0.20, 0.25, 0.35)
    p1.draw_text("When your feature is complete and tested, merge your branch into dev so your teammates get it.", MARGIN_LEFT + 14, y - 42, "F1", 8.5, 0.20, 0.25, 0.35)

    p1.draw_footer()
    pages.append(p1)

    # =========================================================================
    # PAGE 2: Daily Workflow, Committing & Merging with dev
    # =========================================================================
    p2 = PageCanvas(2, 3)
    
    # Page Header Banner
    p2.set_fill_rgb(0.06, 0.09, 0.16)
    p2.draw_rect(MARGIN_LEFT, 770, CONTENT_WIDTH, 42, fill=True)
    p2.set_fill_rgb(0.00, 0.76, 1.00)
    p2.draw_rect(MARGIN_LEFT, 810, CONTENT_WIDTH, 2, fill=True)
    p2.draw_text("DAILY WORKFLOW • SYNCING, COMMITTING & MERGING TO DEV", MARGIN_LEFT + 14, 788, "F2", 11.5, 1.0, 1.0, 1.0)

    # ── Section 3: Daily Morning Routine (dev -> your branch) ──
    y = 746
    p2.draw_text("3. Morning Routine: Syncing with dev (dev -> your branch)", MARGIN_LEFT, y, "F2", 12.0, 0.06, 0.09, 0.16)
    p2.set_stroke_rgb(0.00, 0.76, 1.00)
    p2.set_line_width(1.5)
    p2.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    y -= 16
    p2.draw_text("Before writing any new code, pull teammate updates from dev into your branch:", MARGIN_LEFT, y, "F1", 9, 0.30, 0.35, 0.45)

    y -= 8
    code_box_h = 86
    p2.set_fill_rgb(0.07, 0.10, 0.17)
    p2.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=True)
    p2.set_stroke_rgb(0.20, 0.25, 0.35)
    p2.set_line_width(1.0)
    p2.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=False, stroke=True)

    cy = y - 14
    commands_s3 = [
        ("# Step 1: Switch to dev and fetch newest commits from teammates", (0.58, 0.64, 0.72)),
        ("git checkout dev", (0.22, 0.74, 0.97)),
        ("git pull origin dev", (0.22, 0.74, 0.97)),
        ("# Step 2: Switch back to your personal branch", (0.58, 0.64, 0.72)),
        ("git checkout fullstack/<your-name>", (0.22, 0.74, 0.97)),
        ("# Step 3: Merge dev changes into your working branch", (0.58, 0.64, 0.72)),
        ("git merge dev", (0.98, 0.80, 0.08)),
        ("# Result: Your branch now has all teammate updates!", (0.16, 0.78, 0.45)),
    ]
    for line, col in commands_s3:
        font = "F4" if line.startswith("#") else "F3"
        p2.draw_text(line, MARGIN_LEFT + 12, cy, font, 8.5, *col)
        cy -= 10

    # ── Section 4: Writing Code & Committing Cleanly ──
    y = cy - 20
    p2.draw_text("4. Writing Code & Committing in Your Branch", MARGIN_LEFT, y, "F2", 12.0, 0.06, 0.09, 0.16)
    p2.set_stroke_rgb(0.00, 0.76, 1.00)
    p2.set_line_width(1.5)
    p2.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    y -= 16
    p2.draw_text("Work exclusively on your designated branch. Commit small, logical changes frequently:", MARGIN_LEFT, y, "F1", 9, 0.30, 0.35, 0.45)

    y -= 8
    code_box_h = 76
    p2.set_fill_rgb(0.07, 0.10, 0.17)
    p2.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=True)
    p2.set_stroke_rgb(0.20, 0.25, 0.35)
    p2.set_line_width(1.0)
    p2.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=False, stroke=True)

    cy = y - 14
    commands_s4 = [
        ("# 1. Check modified files", (0.58, 0.64, 0.72)),
        ("git status", (0.22, 0.74, 0.97)),
        ("# 2. Stage your changes", (0.58, 0.64, 0.72)),
        ("git add .", (0.22, 0.74, 0.97)),
        ("# 3. Commit with an explanatory message", (0.58, 0.64, 0.72)),
        ('git commit -m "feat(tokens): integrated P2P token transfer modal"', (0.98, 0.80, 0.08)),
        ("# 4. Push your branch to GitHub backup", (0.58, 0.64, 0.72)),
        ("git push origin fullstack/<your-name>", (0.22, 0.74, 0.97)),
    ]
    for line, col in commands_s4:
        font = "F4" if line.startswith("#") else "F3"
        p2.draw_text(line, MARGIN_LEFT + 12, cy, font, 8.5, *col)
        cy -= 9

    # ── Section 5: Pushing Your Finished Work to dev ──
    y = cy - 20
    p2.draw_text("5. Pushing Finished Work to dev (your branch -> dev)", MARGIN_LEFT, y, "F2", 12.0, 0.06, 0.09, 0.16)
    p2.set_stroke_rgb(0.00, 0.76, 1.00)
    p2.set_line_width(1.5)
    p2.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    y -= 16
    p2.draw_text("When your feature is complete and verified, push it into dev using either method:", MARGIN_LEFT, y, "F1", 9, 0.30, 0.35, 0.45)

    # Method A Box (GitHub PR)
    y -= 10
    pr_box_h = 76
    p2.set_fill_rgb(0.96, 0.98, 1.0)
    p2.draw_rect(MARGIN_LEFT, y - pr_box_h, CONTENT_WIDTH, pr_box_h, fill=True)
    p2.set_stroke_rgb(0.70, 0.82, 0.98)
    p2.set_line_width(0.75)
    p2.draw_rect(MARGIN_LEFT, y - pr_box_h, CONTENT_WIDTH, pr_box_h, fill=False, stroke=True)
    p2.set_fill_rgb(0.14, 0.40, 0.90)
    p2.draw_rect(MARGIN_LEFT, y - pr_box_h, 4, pr_box_h, fill=True)

    p2.draw_text("METHOD A: GITHUB PULL REQUEST (RECOMMENDED & SAFEST)", MARGIN_LEFT + 12, y - 14, "F2", 9, 0.10, 0.30, 0.75)
    p2.draw_text("1. Push your branch: git push origin fullstack/<your-name>", MARGIN_LEFT + 12, y - 28, "F1", 8.5, 0.20, 0.25, 0.35)
    p2.draw_text("2. Go to https://github.com/BohaniLucas/AssetBridge -> Click 'Compare & pull request'", MARGIN_LEFT + 12, y - 41, "F1", 8.5, 0.20, 0.25, 0.35)
    p2.draw_text("3. Target base branch must be 'dev' (NOT main!). Compare branch: 'fullstack/<name>'", MARGIN_LEFT + 12, y - 54, "F2", 8.5, 0.85, 0.25, 0.10)
    p2.draw_text("4. Click 'Create pull request' -> Click 'Merge pull request'. Dev is now updated!", MARGIN_LEFT + 12, y - 67, "F1", 8.5, 0.10, 0.55, 0.25)

    # Method B Box (Terminal Fast Merge)
    y = y - pr_box_h - 14
    code_box_h = 86
    p2.set_fill_rgb(0.07, 0.10, 0.17)
    p2.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=True)
    p2.set_stroke_rgb(0.20, 0.25, 0.35)
    p2.set_line_width(1.0)
    p2.draw_rect(MARGIN_LEFT, y - code_box_h, CONTENT_WIDTH, code_box_h, fill=False, stroke=True)

    cy = y - 14
    commands_s5b = [
        ("# METHOD B: DIRECT TERMINAL MERGE (Fast command line workflow)", (0.58, 0.64, 0.72)),
        ("git push origin fullstack/<your-name>   # Ensure personal branch is pushed", (0.22, 0.74, 0.97)),
        ("git checkout dev                       # Switch to dev branch", (0.22, 0.74, 0.97)),
        ("git pull origin dev                    # Get latest changes from others", (0.22, 0.74, 0.97)),
        ("git merge fullstack/<your-name>        # Merge your finished work into dev", (0.98, 0.80, 0.08)),
        ("git push origin dev                    # Push updated dev to GitHub", (0.16, 0.78, 0.45)),
        ("git checkout fullstack/<your-name>     # Return to your branch for next task", (0.22, 0.74, 0.97)),
    ]
    for line, col in commands_s5b:
        font = "F4" if line.startswith("#") else "F3"
        p2.draw_text(line, MARGIN_LEFT + 12, cy, font, 8.5, *col)
        cy -= 10

    p2.draw_footer()
    pages.append(p2)

    # =========================================================================
    # PAGE 3: Conflict Resolution, Golden Rules & Cheat Sheet
    # =========================================================================
    p3 = PageCanvas(3, 3)
    
    # Page Header Banner
    p3.set_fill_rgb(0.06, 0.09, 0.16)
    p3.draw_rect(MARGIN_LEFT, 770, CONTENT_WIDTH, 42, fill=True)
    p3.set_fill_rgb(0.00, 0.76, 1.00)
    p3.draw_rect(MARGIN_LEFT, 810, CONTENT_WIDTH, 2, fill=True)
    p3.draw_text("CONFLICT RESOLUTION, GOLDEN RULES & QUICK CHEAT SHEET", MARGIN_LEFT + 14, 788, "F2", 11.5, 1.0, 1.0, 1.0)

    # ── Section 6: Handling Merge Conflicts ──
    y = 746
    p3.draw_text("6. How to Resolve Merge Conflicts (No-Panic Guide)", MARGIN_LEFT, y, "F2", 12.0, 0.06, 0.09, 0.16)
    p3.set_stroke_rgb(0.00, 0.76, 1.00)
    p3.set_line_width(1.5)
    p3.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    y -= 14
    p3.draw_text("A conflict only happens when you and a teammate edited the exact same line in the same file.", MARGIN_LEFT, y, "F1", 8.5, 0.30, 0.35, 0.45)
    y -= 12
    p3.draw_text("Git pauses and asks you which version to keep. Here is how to resolve it cleanly in VS Code:", MARGIN_LEFT, y, "F1", 8.5, 0.30, 0.35, 0.45)

    y -= 8
    conflict_box_h = 105
    p3.set_fill_rgb(0.99, 0.95, 0.95)
    p3.draw_rect(MARGIN_LEFT, y - conflict_box_h, CONTENT_WIDTH, conflict_box_h, fill=True)
    p3.set_stroke_rgb(0.95, 0.70, 0.70)
    p3.set_line_width(0.75)
    p3.draw_rect(MARGIN_LEFT, y - conflict_box_h, CONTENT_WIDTH, conflict_box_h, fill=False, stroke=True)
    p3.set_fill_rgb(0.85, 0.20, 0.20)
    p3.draw_rect(MARGIN_LEFT, y - conflict_box_h, 4, conflict_box_h, fill=True)

    p3.draw_text("STEP-BY-STEP CONFLICT RESOLUTION WORKFLOW", MARGIN_LEFT + 12, y - 14, "F2", 9, 0.75, 0.15, 0.15)
    p3.draw_text("1. Open VS Code: Conflicting files are highlighted in purple with an exclamation mark (!).", MARGIN_LEFT + 12, y - 28, "F1", 8.5, 0.20, 0.25, 0.35)
    p3.draw_text("2. Click on the file: Above the highlighted code, VS Code displays 3 clickable helper buttons:", MARGIN_LEFT + 12, y - 41, "F1", 8.5, 0.20, 0.25, 0.35)
    p3.draw_text("   • Accept Current Change: Keeps your version of the code.", MARGIN_LEFT + 20, y - 54, "F2", 8.0, 0.15, 0.45, 0.20)
    p3.draw_text("   • Accept Incoming Change: Keeps your teammate's version from dev.", MARGIN_LEFT + 20, y - 66, "F2", 8.0, 0.20, 0.35, 0.70)
    p3.draw_text("   • Accept Both Changes: Keeps both blocks if both are needed.", MARGIN_LEFT + 20, y - 78, "F2", 8.0, 0.65, 0.45, 0.05)
    p3.draw_text("3. Save file -> git add . -> git commit -m \"fix: resolved merge conflict with dev\" -> Push!", MARGIN_LEFT + 12, y - 94, "F4", 8.0, 0.10, 0.15, 0.25)

    # ── Section 7: Team Golden Rules ──
    y = y - conflict_box_h - 18
    p3.draw_text("7. AssetBridge Team Golden Rules", MARGIN_LEFT, y, "F2", 12.0, 0.06, 0.09, 0.16)
    p3.set_stroke_rgb(0.00, 0.76, 1.00)
    p3.set_line_width(1.5)
    p3.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    rules = [
        ("RULE 1: NEVER PUSH DIRECTLY TO 'main'", "Only the team lead merges 'dev' into 'main' after end-to-end verification.", (0.85, 0.20, 0.20)),
        ("RULE 2: NEVER COMMIT SECRETS OR '.env' FILES", "All API keys and secrets stay in local .env (strictly git-ignored).", (0.80, 0.45, 0.05)),
        ("RULE 3: SYNC WITH 'dev' DAILY", "Frequent small merges prevent large merge headaches. Sync morning & evening.", (0.10, 0.45, 0.75)),
        ("RULE 4: TEST BEFORE PUSHING TO 'dev'", "Run npm test in Public/App and Backend before merging into dev.", (0.15, 0.55, 0.25)),
    ]

    y -= 10
    for r_title, r_desc, col in rules:
        p3.set_fill_rgb(0.97, 0.98, 0.99)
        p3.draw_rect(MARGIN_LEFT, y - 24, CONTENT_WIDTH, 24, fill=True)
        p3.set_stroke_rgb(0.85, 0.88, 0.92)
        p3.set_line_width(0.5)
        p3.draw_rect(MARGIN_LEFT, y - 24, CONTENT_WIDTH, 24, fill=False, stroke=True)
        p3.set_fill_rgb(*col)
        p3.draw_rect(MARGIN_LEFT, y - 24, 3, 24, fill=True)

        p3.draw_text(r_title, MARGIN_LEFT + 10, y - 11, "F2", 8.0, *col)
        p3.draw_text(r_desc, MARGIN_LEFT + 215, y - 11, "F1", 7.8, 0.30, 0.35, 0.42)
        y -= 28

    # ── Section 8: Quick Command Cheat Sheet ──
    y -= 4
    p3.draw_text("8. One-Page Quick Command Cheat Sheet", MARGIN_LEFT, y, "F2", 12.0, 0.06, 0.09, 0.16)
    p3.set_stroke_rgb(0.00, 0.76, 1.00)
    p3.set_line_width(1.5)
    p3.draw_line(MARGIN_LEFT, y - 4, MARGIN_LEFT + CONTENT_WIDTH, y - 4)

    y -= 14
    # Cheat Sheet Table Header
    p3.set_fill_rgb(0.12, 0.16, 0.23)
    p3.draw_rect(MARGIN_LEFT, y - 4, CONTENT_WIDTH, 16, fill=True)
    p3.draw_text("GOAL", MARGIN_LEFT + 8, y, "F2", 8.0, 1.0, 1.0, 1.0)
    p3.draw_text("COMMAND SEQUENCE", MARGIN_LEFT + 180, y, "F2", 8.0, 1.0, 1.0, 1.0)

    cheat_rows = [
        ("See branch & pending files", "git status"),
        ("Download new branches from GitHub", "git fetch origin"),
        ("Switch to your personal branch", "git checkout fullstack/<your-name>"),
        ("Update your branch with team changes", "git checkout dev && git pull && git checkout fullstack/<name> && git merge dev"),
        ("Save & commit your work", 'git add . && git commit -m "description of change"'),
        ("Backup your work to GitHub", "git push origin fullstack/<your-name>"),
        ("Merge your work to dev (Terminal)", "git checkout dev && git pull && git merge fullstack/<name> && git push origin dev"),
        ("Discard local mistakes on a file", "git restore <file-name>"),
    ]

    for goal, cmd in cheat_rows:
        y -= 15
        p3.set_fill_rgb(0.98, 0.99, 1.0)
        p3.draw_rect(MARGIN_LEFT, y - 3, CONTENT_WIDTH, 15, fill=True)
        p3.set_stroke_rgb(0.88, 0.90, 0.94)
        p3.set_line_width(0.5)
        p3.draw_line(MARGIN_LEFT, y - 3, MARGIN_LEFT + CONTENT_WIDTH, y - 3)

        p3.draw_text(goal, MARGIN_LEFT + 8, y + 1, "F2", 7.8, 0.15, 0.20, 0.28)
        p3.draw_text(cmd, MARGIN_LEFT + 180, y + 1, "F4", 7.5, 0.08, 0.38, 0.68)

    p3.draw_footer()
    pages.append(p3)

    # =========================================================================
    # PDF Binary Object Serialization (100% PDF-1.4 Spec Compliant)
    # =========================================================================
    objects = []
    
    # Obj 1: Catalog
    objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    
    # Obj 2: Pages container (kids defined after page objects)
    # Page kids will be objects 3, 4, 5 ...
    # Fonts will be obj 6, 7, 8, 9
    
    font_f1 = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    font_f2 = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>"
    font_f3 = b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>"
    font_f4 = b"<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold >>"
    
    # 4 fonts
    f1_id = 3
    f2_id = 4
    f3_id = 5
    f4_id = 6
    
    page_ids = []
    content_ids = []
    next_id = 7
    
    for i in range(len(pages)):
        page_ids.append(next_id)
        content_ids.append(next_id + 1)
        next_id += 2
        
    pages_obj = f"<< /Type /Pages /Kids [{' '.join(f'{pid} 0 R' for pid in page_ids)}] /Count {len(pages)} >>".encode('ascii')
    
    # Assemble all PDF objects in order
    all_objs = {
        1: objects[0],
        2: pages_obj,
        f1_id: font_f1,
        f2_id: font_f2,
        f3_id: font_f3,
        f4_id: font_f4,
    }
    
    for idx, p in enumerate(pages):
        pid = page_ids[idx]
        cid = content_ids[idx]
        stream_data = "\n".join(p.commands).encode('utf-8')
        
        page_dict = (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_WIDTH:.2f} {PAGE_HEIGHT:.2f}] "
            f"/Resources << /Font << /F1 {f1_id} 0 R /F2 {f2_id} 0 R /F3 {f3_id} 0 R /F4 {f4_id} 0 R >> >> "
            f"/Contents {cid} 0 R >>"
        ).encode('ascii')
        
        content_stream = (
            f"<< /Length {len(stream_data)} >>\nstream\n".encode('ascii') +
            stream_data +
            b"\nendstream"
        )
        
        all_objs[pid] = page_dict
        all_objs[cid] = content_stream

    # Write PDF file with exact byte-offsets and valid xref table
    max_id = max(all_objs.keys())
    out = io.BytesIO()
    out.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    
    offsets = {}
    for oid in range(1, max_id + 1):
        if oid in all_objs:
            offsets[oid] = out.tell()
            out.write(f"{oid} 0 obj\n".encode('ascii'))
            out.write(all_objs[oid])
            out.write(b"\nendobj\n")
            
    xref_offset = out.tell()
    out.write(f"xref\n0 {max_id + 1}\n".encode('ascii'))
    out.write(b"0000000000 65535 f \n")
    for oid in range(1, max_id + 1):
        if oid in offsets:
            out.write(f"{offsets[oid]:010d} 00000 n \n".encode('ascii'))
        else:
            out.write(b"0000000000 00000 f \n")
            
    out.write(f"trailer\n<< /Size {max_id + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n".encode('ascii'))
    
    pdf_bytes = out.getvalue()
    with open(filename, "wb") as f:
        f.write(pdf_bytes)
        
    print(f"SUCCESS: Generated {filename} ({len(pdf_bytes):,} bytes, {len(pages)} pages)")

import io
if __name__ == "__main__":
    out_name = sys.argv[1] if len(sys.argv) > 1 else "AssetBridge_Team_Git_Workflow_Guide.pdf"
    build_pdf(out_name)
