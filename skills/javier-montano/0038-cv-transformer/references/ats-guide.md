# ATS Optimization Deep Dive

## How ATS Systems Parse Resumes

Understanding the parsing logic helps create documents that score 90%+.

### Parsing Pipeline
```
Document Upload → Format Detection → Text Extraction → Section Identification
→ Entity Extraction → Keyword Matching → Score Assignment → Ranking
```

### What ATS Extracts
1. **Contact Information** — Name, email, phone, location, LinkedIn
2. **Work History** — Company, title, dates, descriptions
3. **Education** — Institution, degree, dates, GPA
4. **Skills** — Technical skills, tools, platforms
5. **Certifications** — Name, issuer, date
6. **Keywords** — Matched against job description requirements

### Common Parsing Failures

| Problem | Why It Fails | Solution |
|---------|-------------|----------|
| Tables/columns | ATS reads left-to-right, jumbles multi-column | Single column only |
| Headers/footers | Many ATS skip these entirely | Put all info in body |
| Images/graphics | Can't extract text from images | Use text only |
| Text boxes | Parsed separately, lose context | Standard paragraphs |
| Fancy fonts | May not render, OCR fails | Calibri, Arial, Garamond |
| PDF from design tools | May be image-based, not text | Use .docx |
| Non-standard sections | ATS can't categorize | Standard headers only |
| Merged date formats | "2019-2021" vs "Jan 2019 - Dec 2021" | Use "MM/YYYY — MM/YYYY" |

---

## ATS Scoring Factors

### Keyword Match (40-50% of score)
- Hard skills from job description
- Tools and platforms mentioned
- Certifications required
- Industry-specific terminology

### Experience Relevance (25-30%)
- Job title similarity to target role
- Years of experience match
- Industry alignment
- Progressive career growth

### Education Match (10-15%)
- Degree level meets requirement
- Field of study relevance
- Institution recognition

### Format Quality (10-15%)
- Parseable structure
- Complete contact info
- Consistent date formatting
- Standard section headers

---

## Section Headers — ATS Compatible

Use EXACTLY these headers (ATS systems look for these specific strings):

### English
```
PROFESSIONAL SUMMARY  (or SUMMARY)
PROFESSIONAL EXPERIENCE  (or WORK EXPERIENCE or EXPERIENCE)
EDUCATION
SKILLS  (or TECHNICAL SKILLS or CORE COMPETENCIES)
CERTIFICATIONS  (or CERTIFICATIONS & LICENSES)
LANGUAGES
PUBLICATIONS
VOLUNTEER EXPERIENCE
AWARDS & HONORS
```

### Spanish
```
RESUMEN PROFESIONAL
EXPERIENCIA PROFESIONAL  (or EXPERIENCIA LABORAL)
EDUCACIÓN  (or FORMACIÓN ACADÉMICA)
HABILIDADES  (or COMPETENCIAS TÉCNICAS)
CERTIFICACIONES
IDIOMAS
PUBLICACIONES
EXPERIENCIA VOLUNTARIA
PREMIOS Y RECONOCIMIENTOS
```

---

## Format-Specific ATS Rules

### DOCX (Highest ATS Compatibility)
```
Font: Calibri 10.5pt body, 12pt section headers, 16pt name
Margins: 1 inch all sides (1440 DXA)
Spacing: 6pt after paragraphs, 12pt before sections
Line spacing: 1.15
Bullet: Standard • character
Section divider: 12pt spacing only (no lines if possible)
Alignment: Left (never justify — creates weird spacing)
Bold: Job titles and section headers only
Italic: Company names only (optional)
Underline: Never (ATS may misread)
Color: Black text only (#000000 or #333333)
```

### HTML (For Online Portals)
```html
<!-- Use semantic HTML5 -->
<h1> — Name only
<h2> — Section headers
<h3> — Job titles
<p> — Descriptions
<ul><li> — Achievements
<!-- No JavaScript, no hidden text, no CSS tricks -->
<!-- Schema.org markup for structured data -->
```

### PPTX (For Recruiter Presentations)
```
One section per slide
White background (#FFFFFF)
Black text, Calibri font
No animations, no transitions
Slide 1: Contact + Summary
Slide 2-N: Experience (one role per slide if detailed)
Slide N+1: Education + Certifications
Slide N+2: Skills (organized by category)
```

---

## Keyword Research Method

When the user provides a target role, extract keywords using this method:

1. **Search for 3-5 job postings** for the target role
2. **Extract repeated terms** across postings (skills, tools, qualifications)
3. **Categorize**: Hard skills | Soft skills | Tools | Certifications | Industry terms
4. **Prioritize**: Terms appearing in 3+ postings are mandatory keywords
5. **Map to CV**: Ensure each priority keyword appears 2-3 times naturally

### Universal High-Impact Keywords by Function

**Technology**: Agile, Scrum, CI/CD, Cloud (AWS/Azure/GCP), DevOps, API, Microservices, Machine Learning, Data Analytics, Python, JavaScript, SQL, Kubernetes, Docker

**Marketing**: SEO, SEM, Content Strategy, Marketing Automation, CRM, HubSpot, Google Analytics, Social Media Marketing, Brand Management, Campaign Management, ROI, A/B Testing

**Finance**: Financial Modeling, Forecasting, Budgeting, P&L Management, GAAP, SOX Compliance, Risk Management, Due Diligence, Valuation, M&A, Financial Analysis

**Sales**: Pipeline Management, CRM (Salesforce), Quota Attainment, Business Development, Account Management, Revenue Growth, Negotiation, Strategic Partnerships, SaaS Sales, Enterprise Sales

**HR**: Talent Acquisition, Employee Engagement, Performance Management, HRIS, Compensation & Benefits, Organizational Development, Change Management, Diversity & Inclusion, Succession Planning

**Operations**: Process Improvement, Lean/Six Sigma, Supply Chain, Vendor Management, Project Management (PMP), KPIs, SLA Management, Business Continuity, Quality Assurance
