# Smart Pet Feeder - UML Diagrams

This directory contains all 6 professional UML diagrams for the Smart Pet Feeder IoT system, created using Mermaid syntax.

## 📊 Diagrams Overview

### 1. [Use Case Diagram](./1_use_case_diagram.md)
**Purpose**: Shows all external actors and their interactions with the system  
**Key Elements**:
- 4 Primary Actors (Pet Owner, ESP32, Supabase Auth, Email Service)
- 30 Use Cases across 7 functional groups
- Include/Extend relationships

**Use this for**: Understanding system functionality from user perspective

---

### 2. [Activity Diagram](./2_activity_diagram.md)
**Purpose**: Illustrates the closed-loop feeding control workflow  
**Key Elements**:
- Complete feed command flow from button press to notification
- Decision points for device status, weight tolerance, timeout
- Error handling (SUCCESS, PARTIAL, FAILED states)
- Offline-first command queuing

**Use this for**: Understanding the core FYP feature - closed-loop control

---

### 3. [Sequence Diagram](./3_sequence_diagram.md)
**Purpose**: Shows detailed object interactions during feed command execution  
**Key Elements**:
- 10 Participants (User, Web App, Services, Database, ESP32, Hardware)
- Complete message flow with timing
- Database triggers and real-time updates
- Async operations and WebSocket communication

**Use this for**: Understanding detailed system interactions and timing

---

### 4. [Deployment Diagram](./4_deployment_diagram.md)
**Purpose**: Illustrates physical system architecture and deployment  
**Key Elements**:
- Hardware nodes (Browser, Vercel, Supabase Cloud, ESP32)
- Software components on each node
- Communication protocols (HTTPS, WSS, WiFi, I2C, GPIO, PWM)
- Production deployment architecture

**Use this for**: Understanding how software maps to hardware infrastructure

---

### 5. [Class Diagram](./5_class_diagram.md)
**Purpose**: Shows logical software structure and relationships  
**Key Elements**:
- Frontend classes (Context, Services, Components)
- Backend entities (User, Device, PetProfile, etc.)
- 7 Enumerations for type safety
- Relationships (associations, compositions, dependencies)
- Methods and attributes

**Use this for**: Understanding software architecture and design patterns

---

### 6. [Entity Relationship Diagram (ERD)](./6_entity_relationship_diagram.md)
**Purpose**: Complete database schema with all tables and relationships  
**Key Elements**:
- 8 Tables with full column definitions
- Primary keys, foreign keys, constraints
- Cardinality (1:1, 1:N, N:M)
- ON DELETE CASCADE/SET NULL behaviors
- Indexes, triggers, views
- Row-Level Security policies

**Use this for**: Understanding database design and data model

---

## 🚀 How to Use These Diagrams

### **Option 1: View in Mermaid Live Editor**
1. Go to [mermaid.live](https://mermaid.live)
2. Open any diagram file (e.g., `1_use_case_diagram.md`)
3. Copy the code between the \`\`\`mermaid and \`\`\` tags
4. Paste into Mermaid Live Editor
5. Export as PNG/SVG for your documentation

### **Option 2: View in VS Code**
1. Install "Markdown Preview Mermaid Support" extension
2. Open any diagram file
3. Press `Cmd+Shift+V` (Mac) or `Ctrl+Shift+V` (Windows) for preview
4. Diagrams will render inline

### **Option 3: Include in Documentation**
All diagrams are already formatted as markdown files with:
- Title and description
- Mermaid code block
- Key features explanation

You can directly include them in your project report or presentation.

---

## 📝 Diagram Quality Checklist

All diagrams meet the following criteria:

✅ **Professional**: Uses proper UML notation and conventions  
✅ **Well-structured**: Logical grouping and clear layout  
✅ **Clean**: Not cluttered, readable labels and text  
✅ **Accurate**: Reflects actual implementation, not assumptions  
✅ **Complete**: Includes all critical components and relationships  

---

## 🎓 For Your FYP Report

### **Recommended Usage**

1. **Introduction Section**: Use Case Diagram
   - Shows complete system functionality
   - Demonstrates scope of project

2. **System Design Section**: 
   - Activity Diagram (closed-loop control)
   - Deployment Diagram (architecture)
   - Class Diagram (software design)

3. **Implementation Section**:
   - Sequence Diagram (detailed interactions)
   - ERD (database implementation)

4. **Appendix**: All diagrams for reference

### **Diagram Descriptions for Report**

Each diagram file includes:
- **Description**: What the diagram shows
- **Key Features**: Important elements highlighted
- **Use Case**: When to reference this diagram

Copy these descriptions into your report to explain each diagram.

---

## 🔧 Technical Details

### **Technology Stack Shown**
- **Frontend**: React 19.2.0, Vite, React Router
- **Backend**: Supabase (PostgreSQL, Auth, Realtime)
- **IoT**: ESP32, HX711 Load Cell, Servo Motor, Ultrasonic Sensors
- **Protocols**: HTTPS, WebSocket, WiFi, I2C, GPIO, PWM

### **Key Features Illustrated**
- Offline-first command queuing
- Closed-loop control with weight feedback
- Real-time updates via WebSocket
- Row-Level Security (RLS)
- Database triggers and views
- Multi-caregiver support (future)

---

## 📚 Additional Resources

- **Project Proposal**: `../Adarsha Prasai Proposal.txt`
- **Literature Review**: `../Adarsha Prasai Literature Review.txt`
- **System Architecture**: `../system_architecture.md.resolved`
- **Database Schema**: `../supabase/migrations/001_initial_schema.sql`
- **Technical Prompt**: `../NOTEBOOKLM_DIAGRAM_PROMPT.md`

---

## 📄 License

These diagrams are part of the Smart Pet Feeder Final Year Project by Adarsha Prasai (2408599).

---

**Created**: December 13, 2025  
**Author**: Adarsha Prasai  
**Project**: IoT-Enabled Smart Pet Feeder with Closed-Loop Control  
**Institution**: Herald College Kathmandu
