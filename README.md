# Academic Projects & Achievements

Welcome to my portfolio of academic projects. These projects span across database management, distributed systems, and artificial intelligence, reflecting the skills and knowledge I've acquired throughout my Computer Science studies at the University of Manchester.

## Table of Contents
- [Database Management](#database-management)
- [Distributed Systems](#distributed-systems)
- [Artificial Intelligence](#artificial-intelligence)

---

## Database Management
### Architected Database Schema for a Business Application
- **Description**: Engineered and fine-tuned a robust database schema for a sizable enterprise, handling data for 500+ employees and reducing redundancy by 40%.
- **Technologies**: Normalization (1NF, 2NF, 3NF)
- **Images**:
  - ![Database Schema Image 1](path-to-image-1.png)
  - ![Database Schema Image 2](path-to-image-2.png)
- **Documentation**: [Database Schema PDF](path-to-pdf.pdf)

### End-to-End System Development
- **Description**: Developed a scalable backend with PHP and MySQL and an intuitive frontend, ensuring functionality, security, and performance.
- **Technologies**: PHP, MySQL, Frontend Technologies
- **Images**:
  - ![End-to-End Development Image 1](path-to-image-1.png)
  - ![End-to-End Development Image 2](path-to-image-2.png)

---

## Distributed Systems
### Real-Time Messaging for Healthcare
- **Description**: Created a client-server messaging platform for real-time communication among healthcare professionals.
- **Technologies**: Python, Client-Server Architecture
- **Images**:
  - ![Real-Time Messaging Image 1](path-to-image-1.png)
  - ![Real-Time Messaging Image 2](path-to-image-2.png)


### Scalable Multi-User Messaging Enhancement for Healthcare
- **Description**: Enhanced a messaging system to support concurrent users with features like registration and customizable nicknames.
- **Technologies**: Python, Scalability Techniques
- **Images**:
  - ![Scalable Messaging Image 1](path-to-image-1.png)
  - ![Scalable Messaging Image 2](path-to-image-2.png)

### Distributed Wedding Planner Application with Concurrency Management
- **Description**: Developed an SOA-driven system for wedding scheduling, managing up to 550 concurrent users/bots reservations.
- **Technologies**: Python, SOA, Concurrency
- **Images**:
  - ![Wedding Planner Image 1](path-to-image-1.png)
  - ![Wedding Planner Image 2](path-to-image-2.png)

---

## Artificial Intelligence
### Reversi Game AI with Mini-Max Optimization
- **Description**: Implemented an advanced AI for Reversi using Java, achieving high win rates against human players and peer AIs.
- **Technologies**: Java, Mini-Max with Alpha-Beta Pruning
- **Images**:
  - ![Reversi AI Image 1](/Users/thebekhruz/Desktop/CV_Projects/resources/reversi1.png)
  - ![Reversi AI Image 2](/Users/thebekhruz/Desktop/CV_Projects/resources/reversi2.png.png)

### Intelligent Washing Machine with Fuzzy Logic
- **Description**: Created an intelligent system for a washing machine using fuzzy logic to optimize wash parameters.
- **Technologies**: Python, Fuzzy Logic
- **Images**:
```
def configure_washing_machine(dirt_amount: float, fabric_weight: float) -> tuple:
    all_antecedents = [] # this should be set to a List containing the antecedent values for all rules
    all_outputs = [] # this should be set to a List containing the output values for all rules
 
 
    r1 = get_rule_antecedent_value(None, 0.0, very_delicate_set, fabric_weight, "")
    r2 = get_rule_antecedent_value(delicate_set, fabric_weight, almost_clean_set, dirt_amount, "OR" )
    r3 = get_rule_antecedent_value(delicate_set, fabric_weight, dirty_set, dirt_amount, "AND" )
    r4 = get_rule_antecedent_value(not_delicate_set, fabric_weight, dirty_set, dirt_amount, "AND" )
    
    all_antecedents.append(r1)
    all_antecedents.append(r2)
    all_antecedents.append(r3)
    all_antecedents.append(r4)
    
    o1 = get_rule_output_value(1,r1)
    o2 = get_rule_output_value(2,r2)
    o3 = get_rule_output_value(3,r3)
    o4 = get_rule_output_value(4,r4)
    
    all_outputs.append(o1)
    all_outputs.append(o2)
    all_outputs.append(o3)
    all_outputs.append(o4)
    return (all_antecedents, all_outputs)
```

---

## How to Use This Repository
To view the projects, please navigate through the folders structured as per the categories mentioned above. For detailed explanations and visual illustrations, refer to the linked PDF documents and images provided within each project's directory.