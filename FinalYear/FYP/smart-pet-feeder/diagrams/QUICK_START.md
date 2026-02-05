# Quick Start Guide - Using Your Diagrams

## 🎯 Immediate Next Steps

### 1. **Test the Diagrams** (2 minutes)

Go to [mermaid.live](https://mermaid.live) and test one diagram:

1. Open `diagrams/1_use_case_diagram.md`
2. Copy everything between \`\`\`mermaid and \`\`\`
3. Paste into Mermaid Live Editor
4. Verify it renders correctly

### 2. **Export for Your Report** (5 minutes)

For each diagram you want to use:

1. Paste code into [mermaid.live](https://mermaid.live)
2. Click "Actions" → "PNG" or "SVG"
3. Download the image
4. Insert into your FYP report

### 3. **Customize if Needed** (optional)

All diagrams are editable. Common customizations:

```mermaid
%% Change colors
style NodeName fill:#4F46E5,stroke:#312E81,color:#fff

%% Add notes
Note over Component: This is a note

%% Adjust layout
direction TB  %% Top to Bottom
direction LR  %% Left to Right
```

---

## 📊 Which Diagram to Use When

### **For Proposal/Initial Design**
- ✅ Use Case Diagram - Shows what the system does
- ✅ Deployment Diagram - Shows hardware/software architecture

### **For Detailed Design**
- ✅ Activity Diagram - Shows closed-loop control (core FYP feature)
- ✅ Class Diagram - Shows software structure
- ✅ ERD - Shows database design

### **For Implementation Explanation**
- ✅ Sequence Diagram - Shows how components interact
- ✅ Activity Diagram - Shows workflow step-by-step

### **For Final Report**
- ✅ All 6 diagrams in appropriate sections

---

## 🎓 For Your FYP Report

### **Suggested Report Structure**

```
Chapter 3: System Design
├── 3.1 System Overview
│   └── Use Case Diagram
├── 3.2 System Architecture
│   └── Deployment Diagram
├── 3.3 Software Design
│   ├── Class Diagram
│   └── Activity Diagram (Closed-Loop Control)
└── 3.4 Database Design
    └── Entity Relationship Diagram

Chapter 4: Implementation
├── 4.1 Feed Command Flow
│   └── Sequence Diagram
└── 4.2 Closed-Loop Control Implementation
    └── Activity Diagram (reference again)
```

### **Sample Diagram Captions**

```
Figure 3.1: Use Case Diagram showing all system actors and their interactions 
with the Smart Pet Feeder system. The diagram illustrates 30 use cases across 
7 functional groups including user management, device operations, and feeding 
control.

Figure 3.2: Activity Diagram illustrating the closed-loop feeding control 
workflow. The diagram shows decision points for device status, weight 
tolerance checking, and error handling with SUCCESS, PARTIAL, and FAILED 
states.

Figure 3.3: Sequence Diagram showing detailed object interactions during 
feed command execution. The diagram includes 10 participants and demonstrates 
the complete message flow from user button press to notification delivery, 
including database triggers and real-time WebSocket updates.

Figure 3.4: Deployment Diagram illustrating the physical system architecture. 
The diagram shows how software components are distributed across hardware 
nodes including user's browser, Vercel cloud hosting, Supabase backend, and 
ESP32 IoT device.

Figure 3.5: Class Diagram showing the logical software structure. The diagram 
includes frontend components, service layers, and backend entities with their 
relationships, attributes, and methods.

Figure 3.6: Entity Relationship Diagram (ERD) showing the complete database 
schema. The diagram includes 8 tables with full column definitions, primary 
and foreign keys, cardinality relationships, and cascade behaviors.
```

---

## 🔍 Diagram Quality Check

Before submitting, verify each diagram:

- [ ] Renders correctly in Mermaid Live
- [ ] All text is readable (not too small)
- [ ] Colors are professional (not too bright)
- [ ] Relationships are clear
- [ ] Labels are descriptive
- [ ] No overlapping elements

---

## 💡 Pro Tips

### **Tip 1: High-Resolution Exports**
When exporting from Mermaid Live:
- Use SVG format for best quality (scales infinitely)
- Or use PNG at 2x or 3x scale for high DPI

### **Tip 2: Consistent Styling**
All diagrams use consistent color scheme:
- Blue (#4F46E5): Primary components
- Green (#10B981): Success/Active states
- Orange (#F59E0B): Warnings/Pending
- Red (#EF4444): Errors/Failed states

### **Tip 3: Diagram Descriptions**
Each diagram file includes:
- Title
- Description
- Key features
- Mermaid code

Copy the descriptions into your report!

### **Tip 4: Update as You Build**
As you implement features:
1. Update the relevant diagram
2. Re-export the image
3. Replace in your report

This keeps documentation in sync with code.

---

## 🚀 Advanced: Embedding in Markdown

If your report supports Mermaid (like GitHub, GitLab, or some LaTeX templates):

```markdown
## System Architecture

The following diagram shows our deployment architecture:

\`\`\`mermaid
graph TB
    Browser[Web Browser] --> Vercel[Vercel Hosting]
    Vercel --> Supabase[Supabase Backend]
    ESP32[ESP32 Device] --> Supabase
\`\`\`
```

The diagram will render automatically!

---

## 📞 Need Help?

### **Common Issues**

**Issue**: Diagram doesn't render in Mermaid Live  
**Solution**: Check for syntax errors, especially in quotes and brackets

**Issue**: Text is too small  
**Solution**: Reduce number of nodes or split into multiple diagrams

**Issue**: Layout is messy  
**Solution**: Try changing `direction TB` to `direction LR` or vice versa

**Issue**: Colors don't match  
**Solution**: Use the style definitions at the bottom of each diagram

---

## ✅ Checklist for FYP Submission

- [ ] All 6 diagrams tested in Mermaid Live
- [ ] Diagrams exported as high-quality images
- [ ] Diagrams inserted into report with captions
- [ ] Diagram descriptions added to report text
- [ ] Diagrams referenced in text (e.g., "as shown in Figure 3.1")
- [ ] Consistent formatting across all diagrams
- [ ] Source code (.md files) backed up

---

**You're all set! 🎉**

Your diagrams are professional, comprehensive, and ready for your FYP report. Good luck with your project!
