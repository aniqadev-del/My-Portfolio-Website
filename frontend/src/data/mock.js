// Mock data for SoftGemZ website

export const companyInfo = {
  name: "SoftGemZ",
  tagline: "AI & Automation Solutions",
  description: "At SoftGemZ, we combine AI + Automation to help businesses save time, reduce errors, and work smarter. From automating calibration workflows to building AI-powered dashboards, our mission is to design solutions that give you more time to focus on what matters most.",
  logo: "https://customer-assets.emergentagent.com/job_5f6418a6-b95d-48bd-8557-c249c328e302/artifacts/zwg1ymxj_Logo%20Final.png"
};

export const services = [
  {
    id: 1,
    title: "Process Automation",
    description: "Streamline repetitive tasks with intelligent workflow automation using Power Automate and custom solutions.",
    icon: "Zap",
    features: [
      "Document processing automation",
      "Email & notification workflows", 
      "Data entry elimination",
      "Compliance management"
    ]
  },
  {
    id: 2,
    title: "AI-Powered Analytics",
    description: "Transform your data into actionable insights with custom AI models and predictive analytics.",
    icon: "Brain",
    features: [
      "Business intelligence dashboards",
      "Predictive modeling",
      "Anomaly detection",
      "Real-time reporting"
    ]
  },
  {
    id: 3,
    title: "Document Intelligence",
    description: "Extract and process information from unstructured documents using advanced AI techniques.",
    icon: "FileText",
    features: [
      "Automated data extraction",
      "Document classification",
      "Template standardization",
      "Quality assurance workflows"
    ]
  },
  {
    id: 4,
    title: "Custom Software Development",
    description: "Build tailored software solutions that integrate seamlessly with your existing systems.",
    icon: "Code",
    features: [
      "Web applications",
      "API integrations",
      "Database optimization",
      "System modernization"
    ]
  }
];

export const portfolioProjects = [
  {
    id: 1,
    title: "Calibration Certificate Automation",
    category: "Process Automation",
    description: "Eliminated repetitive manual work in calibration management by building a Power Automate workflow that generated 25+ calibration certificates monthly.",
    challenge: "Manual data entry for calibration certificates was time-consuming and error-prone",
    solution: "Built a Power Automate workflow that pulled data directly from a master sheet (instrument ID, model, manufacturer, reference values) and prefilled templates automatically.",
    impact: "Reduced manual data entry by 90%, ensured compliance, and saved technicians hours every month.",
    technologies: ["Power Automate", "Microsoft 365", "Data Integration"],
    mockImage: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600&h=400&fit=crop"
  },
  {
    id: 2,
    title: "Weekly Calibration Expiry Alerts",
    category: "Compliance Management",
    description: "Ensured timely calibration compliance across hundreds of instruments with automated alert system.",
    challenge: "Risk of missed calibrations due to lack of proactive monitoring",
    solution: "Created a Power Automate solution that scanned the calibration master sheet weekly, identified upcoming expiry dates, and sent proactive email alerts.",
    impact: "Improved audit readiness, reduced missed calibrations, and strengthened operational reliability.",
    technologies: ["Power Automate", "Email Integration", "Data Analytics"],
    mockImage: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=600&h=400&fit=crop"
  },
  {
    id: 3,
    title: "Document Formatting Automation",
    category: "AI-Assisted Processing",
    description: "Standardized unstructured lab reports into consistent templates using AI-driven document processing.",
    challenge: "Lab reports came in various formats, requiring manual standardization",
    solution: "Designed an AI-driven document processing workflow that extracted key values from raw lab documents and reformatted them into ready-to-use certificate templates.",
    impact: "Eliminated manual copy-pasting, improved consistency, and accelerated reporting turnaround.",
    technologies: ["AI Document Processing", "Template Engine", "Data Extraction"],
    mockImage: "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=600&h=400&fit=crop"
  },
  {
    id: 4,
    title: "Automated Invoicing & Reminders",
    category: "Business Process Automation",
    description: "Simplified client billing and follow-ups with intelligent invoicing workflows.",
    challenge: "Manual invoice generation and follow-ups were consuming admin resources",
    solution: "Implemented a workflow where invoices were automatically generated from client bookings and sent via email, with payment reminders and cancellation rules if overdue.",
    impact: "Reduced admin workload, improved payment timelines, and created a seamless client experience.",
    technologies: ["Workflow Automation", "Email Marketing", "Payment Integration"],
    mockImage: "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=400&fit=crop"
  },
  {
    id: 5,
    title: "Business Intelligence Dashboard",
    category: "AI-Powered Analytics",
    description: "Provided management with real-time visibility into operations using AI-powered insights.",
    challenge: "Management lacked real-time visibility into operational performance",
    solution: "Developed a Power BI dashboard integrated with Microsoft 365 and Power Automate, providing predictive insights and highlighting anomalies using AI models.",
    impact: "Enabled smarter decision-making with real-time analytics and reduced reliance on manual reporting.",
    technologies: ["Power BI", "AI Models", "Microsoft 365", "Predictive Analytics"],
    mockImage: "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop"
  }
];

export const testimonials = [
  {
    id: 1,
    name: "Sarah Johnson",
    position: "Operations Manager",
    company: "TechCorp Industries",
    content: "SoftGemZ transformed our calibration process completely. What used to take hours now happens automatically. The ROI was immediate.",
    rating: 5
  },
  {
    id: 2,
    name: "Michael Chen",
    position: "CTO",
    company: "InnovateNow",
    content: "Their AI-powered document processing solution saved us 20+ hours per week. Exceptional technical expertise and delivery.",
    rating: 5
  },
  {
    id: 3,
    name: "Emily Rodriguez",
    position: "Business Owner",
    company: "QuickBooks Consulting",
    content: "The automated invoicing system has streamlined our entire billing process. Professional, reliable, and results-driven.",
    rating: 5
  }
];

export const contactInfo = {
  email: "hello@softgemz.com",
  phone: "+1 (555) 123-4567",
  address: "123 Innovation Drive, Tech City, TC 12345",
  socialMedia: {
    instagram: "https://www.instagram.com/aniqasoftgemz/",
    linkedin: "https://www.linkedin.com/in/aniqa-ilyas-patel-609a24384/",
    twitter: "https://x.com/AniqaPatel"
  },
  whatsapp: "+1-555-123-4567"
};

export const stats = [
  { label: "Projects Completed", value: "50+", icon: "CheckCircle" },
  { label: "Hours Saved Monthly", value: "500+", icon: "Clock" },
  { label: "Happy Clients", value: "25+", icon: "Users" },
  { label: "Automation Success Rate", value: "95%", icon: "TrendingUp" }
];