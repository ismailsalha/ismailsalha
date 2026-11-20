"""Everything the profile says. Copy and numbers mirror the portfolio (ismailsalha.vercel.app)."""

LOGIN = "ismailsalha"
NAME = "Ismail Salha"
NAME_AR = "إسماعيل صالحة"
ROLE = "Computer & Intelligent Systems Engineer"
LOCATION = "Gaza, Palestine"
PORTFOLIO = "https://ismailsalha.vercel.app"
EMAIL = "ismailsalha21@gmail.com"
LINKEDIN = "https://www.linkedin.com/in/ismail-salha-b571633b6"
INSTAGRAM = "https://instagram.com/ismail.sal7a"

FOCUS = ["Machine Learning", "Data Analysis", "Web Development", "Cybersecurity Enthusiast"]
INTRO = ("Building intelligent systems, data-driven solutions and clean web experiences at the "
         "intersection of engineering and design. Based in Gaza, Palestine.")
OPEN_TO = ["Internships", "Freelance work", "Collaborations"]
HERO_CHIPS = ["Python", "TensorFlow", "SQL", "FastAPI"]
HERO_STATS = [
    ("07", "Projects in my portfolio", "outline"),
    ("GDG", "Core team, GDGoC Al-Aqsa", "fg"),
    ("AI / ML", "Primary focus", "fg"),
    ("Gaza", "Based in Palestine", "amber"),
]

ABOUT = [
    "I'm **Ismail Salha**, a Computer & Intelligent Systems Engineer from Gaza, Palestine, working across "
    "machine learning, data analysis, web development and cybersecurity.",
    "I enjoy turning raw data into clear insight, training and evaluating models honestly, and shipping fast, "
    "accessible web interfaces that people actually like to use.",
    "Outside my own projects I'm an **IEEE Student Member** (Palestine Subsection) and a **Core Team member of "
    "GDGoC Al-Aqsa**, helping grow the local tech community.",
]

TOOLKIT = [
    ("A.01", "AI & Machine Learning", "network", ["Python", "scikit-learn", "pandas", "NumPy", "TensorFlow"]),
    ("A.02", "Data", "chart", ["SQL", "Power BI", "Data Visualization", "Matplotlib", "Seaborn"]),
    ("A.03", "Web Development", "code", ["HTML", "CSS", "JavaScript", "React", "Next.js", "FastAPI"]),
    ("A.04", "Security & Tools", "shield", ["Network Security", "Linux", "OWASP Top 10", "Git", "n8n", "Docker"]),
]

MARQUEE_TOOLS = ["Python", "scikit-learn", "pandas", "NumPy", "TensorFlow", "SQL", "Power BI",
                 "Data Visualization", "Matplotlib", "React", "Next.js", "FastAPI", "Linux", "Docker", "n8n"]
MARQUEE_AREAS = ["Machine Learning", "Data Analysis", "Web Development", "APIs & Backend", "Cybersecurity", "Automation"]

FEATURED = {
    "key": "radar",
    "num": "01",
    "kind": "AI Product",
    "title": "Radar Forsa",
    "title_ar": "رادار الفرص",
    "meta": [("lock", "Private code"), ("dot", "JavaScript")],
    "role": "Solo project",
    "text": ("A serverless bot that finds scholarships for Palestinian students. It watches 7 RSS feeds, has "
             "Gemini read every call (who can apply, the deadline, the funding and the scam risk), drops "
             "duplicates and posts the best calls in Arabic to three Telegram channels, with reminders before "
             "each deadline. It runs free on Cloudflare Workers."),
    "stack": ["Cloudflare Workers", "D1", "Gemini", "Telegram Bot API"],
    "cta": "Open the Telegram channel",
    "channels": [("radar-general", "Every opportunity", "@radar_forsa"),
                 ("radar-masters", "Master's", "@radar_forsamasters"),
                 ("radar-phd", "PhD", "@radar_forsaPHD")],
    "metrics": [("3", "Telegram channels", "cyan"), ("480", "Runs a day", "fg"),
                ("75", "End-to-end checks", "fg"), ("$0", "Cost a month", "amber")],
    "href": "https://t.me/radar_forsa",
}

PRODUCTS = [
    {
        "key": "nashrati", "num": "02", "kind": "AI Product", "title": "Nashrati AI",
        "meta": [("lock", "Private code"), ("dot", "Python")],
        "role": "Team project · my part: the AI service",
        "text": ("A newsroom platform that turns a reporter's field recording into a news draft. Arabic speech "
                 "is transcribed, then drafted with AI from the transcript, the notes, the place and the date. "
                 "Editors review and approve it in a dual-panel workspace."),
        "stack": ["FastAPI", "Azure AI Speech", "Laravel", "React", "Flutter"],
        "metrics": [("5", "User roles", "cyan"), ("4", "Parts", "fg"), ("AR", "Speech to text", "amber")],
        "cta": "Visit the website",
        "href": "https://nashrati.online",
    },
    {
        "key": "solar", "num": "03", "kind": "Telegram Bot", "title": "Solar Power",
        "meta": [("lock", "Private code"), ("dot", "TypeScript")],
        "role": "Team of two · my part: the forecast engine",
        "text": ("A free Telegram bot for homes in Gaza. Every morning it forecasts how much the solar panels "
                 "will produce hour by hour, when the battery will be full and the best time for heavy "
                 "appliances. One tap each evening teaches it each home's correction factor."),
        "stack": ["TypeScript", "Cloudflare Workers", "D1", "Open-Meteo"],
        "metrics": [("06:30", "Morning forecast", "cyan"), ("24h", "Hourly output", "fg"), ("1", "Tap a day", "amber")],
        "cta": "See it in my portfolio",
        "href": PORTFOLIO + "/#projects",
    },
]

SOLAR_MORNING = [("sun", "صباح الخير! اليوم مشمس", True), ("zap", "إنتاجك حوالي 14 كيلوواط ساعة", False),
                 (None, "bars", False), ("battery", "بطاريتك بتمتلي حوالي الساعة 12 ونص الظهر", False),
                 ("washer", "أحسن وقت للغسالة: من 11 لـ 2", False)]
SOLAR_EVENING = "مسا الخير! امتلت بطاريتك اليوم؟"
SOLAR_ANSWERS = ["قبل الظهر", "الظهر", "العصر", "ما امتلت"]
SOLAR_LEVELS = [2, 4, 6, 7, 8, 8, 7, 6, 4, 2]

REPOS = [
    {
        "key": "ml-finalproject1", "num": "04", "kind": "Machine Learning", "title": "Social Network User Grouping",
        "repo": "ML-Finalproject1", "lang": "Jupyter Notebook",
        "text": ("Unsupervised learning that segments 8,878 social media users into behavioral groups from their "
                 "usage habits. Compares K-Means, DBSCAN and Mean Shift, with PCA visuals."),
        "stack": ["Python", "scikit-learn", "pandas", "Seaborn"],
        "metrics": [("8,878", "Users"), ("3", "Algorithms"), ("0.141", "Silhouette")],
    },
    {
        "key": "ismail_salha_project", "num": "05", "kind": "Web Development", "title": "Smile Dental Clinic Website",
        "repo": "Ismail_Salha_Project", "lang": "HTML",
        "text": ("A responsive Arabic (RTL) website for a dental clinic with services and prices, appointment "
                 "booking, visit details, a patient record form and a contact page."),
        "stack": ["HTML", "CSS", "JavaScript"],
        "metrics": [("6", "Pages"), ("RTL", "Arabic layout"), ("Booking", "Appointments")],
    },
    {
        "key": "pattern_recognition_research_report", "num": "06", "kind": "Research",
        "title": "The Illusion of High Accuracy", "repo": "Pattern_Recognition_Research_Report", "lang": None,
        "text": ("Research report on why high accuracy can mislead in pattern recognition: class imbalance, data "
                 "leakage and overfitting, with a multi-metric evaluation framework."),
        "stack": ["Pattern Recognition", "Model Evaluation"],
        "metrics": [("99%", "Trivial accuracy"), ("1:100", "Imbalance"), ("10-fold", "Stratified CV")],
    },
    {
        "key": "ismailsalhaassignment1preprocessingnew", "num": "07", "kind": "Data Analysis",
        "title": "House Prices Data Preprocessing", "repo": "ismailsalhaAssignment1Preprocessingnew",
        "lang": "Jupyter Notebook",
        "text": ("Preparing the Kaggle House Prices dataset for modeling: missing values, outliers, a log target, "
                 "feature engineering, encoding and a scikit-learn pipeline."),
        "stack": ["Python", "pandas", "scikit-learn", "Colab"],
        "metrics": [("1,460", "Homes"), ("81", "Columns"), ("TotalSF", "New feature")],
    },
]

EXPERIENCE = [
    {"code": "E-01", "org": "GDGoC Al-Aqsa", "title": "Core Team Member", "warm": False, "art": "network",
     "text": "Organizing workshops and tech events for students on Google technologies.",
     "tags": ["Workshops", "Tech events", "Google technologies"]},
    {"code": "E-02", "org": "IEEE Palestine Subsection", "title": "IEEE Student Member", "warm": True, "art": "wave",
     "text": "Active member participating in technical activities and professional development.",
     "tags": ["Technical activities", "Professional development"]},
]

CONTACT_TEXT = ("I'm open to internships, freelance work and collaborations in machine learning, data and web "
                "development. Email me and I'll get back to you.")
CHANNELS = [
    ("mail", "Email", EMAIL, "mailto:" + EMAIL),
    ("linkedin", "LinkedIn", "in/ismail-salha-b571633b6", LINKEDIN),
    ("globe", "Portfolio", "ismailsalha.vercel.app", PORTFOLIO),
    ("instagram", "Instagram", "@ismail.sal7a", INSTAGRAM),
]
