# Contract Analysis & Report Feature

## 🎯 Overview

The Expiring Contracts page now features AI-powered contract analysis and report generation. This feature allows users to generate detailed analysis reports for any contract using OpenAI's AI capabilities.

## ✨ Features

### 📊 **Contract Analysis Reports**
- Generate AI-powered analysis for any contract
- Get detailed recommendations and alternatives
- View markdown-formatted reports with proper styling
- Real-time generation with loading indicators

### 🔍 **Report Contents**
Each generated report includes:
1. **Current Contract Overview** - Analysis, strengths, and limitations
2. **Requirements Analysis** - User needs and current suitability
3. **Similar Services in the Market** - Comparison with alternatives
4. **Recommendations** - Most suitable solutions and implementation roadmap

### 🎨 **User Interface**

#### Main Page
- **Title**: "Contract Analysis & Reports"
- **Info Alert**: Shows total contracts and demo mode message
- **Table**: Displays all contracts with "Generate Report" button
- **Contract Info**: Uses ContractRow component for detailed display

#### Report Modal
- **Width**: 1200px for comfortable reading
- **Loading State**: Animated spinner with AI analysis message
- **Contract Details Card**: Shows contract information at top
- **Analysis Card**: Beautifully formatted markdown report
- **Status Tag**: Shows expired/expiring status
- **Scrollable**: Auto-scroll for long reports

## 🚀 How It Works

### Technical Flow
```
User clicks "Generate Report"
    ↓
Modal opens with loading state
    ↓
API call to /api/v1/contracts/alerts/expiring
    ↓
Backend uses OpenAI with web search
    ↓
AI analyzes contract and finds alternatives
    ↓
Returns markdown-formatted report
    ↓
Display with ReactMarkdown component
```

### API Integration
```javascript
GET /api/v1/contracts/alerts/expiring?user_email={email}

Response:
{
  "success": true,
  "user_email": "user@example.com",
  "count": 5,
  "data": [
    {
      "contract_id": "contract_123",
      "expired_status": "near_expiry",
      "report": "## CURRENT CONTRACT OVERVIEW\n\n..."
    }
  ]
}
```

## 📋 Usage Guide

### Step 1: Navigate to Expiring Contracts
- Click on "Expiring Contracts" in the sidebar
- Page shows all contracts in demo mode

### Step 2: Generate Report
- Find the contract you want to analyze
- Click the "Generate Report" button
- Modal opens with loading state

### Step 3: Wait for Analysis
- AI analyzes the contract (30-60 seconds)
- Shows animated loading indicator
- Displays progress message

### Step 4: View Report
- Report appears in beautiful markdown format
- Scroll through sections:
  - Overview
  - Requirements
  - Market alternatives
  - Recommendations

### Step 5: Close Modal
- Click "Close" button to exit
- Report is not saved (regenerate when needed)

## 🎨 UI Components

### Markdown Styling
- **H1/H2**: Blue color (#1890ff) for main headings
- **H3/H4**: Dark blue (#2c3e50) for sub-headings
- **Paragraphs**: 1.8 line height for readability
- **Lists**: Proper indentation and spacing
- **Strong text**: Blue color for emphasis
- **Code**: Gray background with proper formatting

### Status Tags
- **Red**: Expired contracts
- **Orange**: Expiring soon (within 60 days)
- **Blue**: Missing end date

### Icons
- **FileSearchOutlined**: Report and analysis
- **LoadingOutlined**: Loading state
- **CheckCircleOutlined**: Success status

## 🔧 Technical Implementation

### State Management
```javascript
const [selectedContract, setSelectedContract] = useState(null);
const [reportModalVisible, setReportModalVisible] = useState(false);
const [generatingReport, setGeneratingReport] = useState(false);
const [contractReport, setContractReport] = useState(null);
```

### Key Functions

#### handleGenerateReport
- Opens modal
- Sets loading state
- Calls API
- Finds specific contract report
- Displays result or error

#### ReactMarkdown Component
- Custom styling for all markdown elements
- Proper spacing and colors
- Responsive design
- Code block formatting

### Dependencies Added
```json
{
  "react-markdown": "^9.0.1"
}
```

## 🎯 Benefits

### For Users
- **Quick insights**: Get AI analysis in seconds
- **Informed decisions**: See market alternatives
- **Professional reports**: Well-formatted, easy to read
- **No manual research**: AI does web search automatically

### For Business
- **Cost optimization**: Find better alternatives
- **Risk management**: Identify expiring contracts
- **Vendor comparison**: See similar services
- **Strategic planning**: Get implementation roadmaps

## 📊 Example Report Structure

```markdown
## TỔNG QUAN HỢP ĐỒNG HIỆN TẠI

Phân tích chi tiết về hợp đồng hiện tại...

## PHÂN TÍCH YÊU CẦU

Các yêu cầu và đánh giá...

## DỊCH VỤ TƯƠNG TỰ TRÊN THỊ TRƯỜNG

1. **Alternative 1**
   - Pros: ...
   - Cons: ...
   - Pricing: ...

2. **Alternative 2**
   - ...

## KHUYẾN NGHỊ

Giải pháp được đề xuất và roadmap triển khai...
```

## 🔒 Security & Performance

### Security
- User email required for API calls
- Reports generated per-request (not stored)
- No sensitive data in client state

### Performance
- API timeout: 60 seconds (AI generation)
- Report caching: Not implemented (generate on demand)
- Modal lazy loading: Only loads when opened
- Markdown rendering: Efficient with ReactMarkdown

## 🎉 Demo Mode

### Why Show All Contracts?
- Easy to test with any contract
- Show full system capabilities
- No need to wait for expiry
- Better for demonstrations

### Production Mode
To switch to production mode (show only expiring):
```javascript
// Change from:
const { contracts, loading } = useContract();

// To:
const { expiringContracts, loading } = useContract();
```

## 🚀 Future Enhancements

Potential improvements:
- **Cache reports**: Store generated reports
- **Export PDF**: Download report as PDF
- **Email reports**: Send to stakeholders
- **Scheduled reports**: Auto-generate monthly
- **Batch analysis**: Analyze multiple contracts
- **Custom prompts**: User-defined analysis criteria
- **Report history**: Track previous reports
- **Comparison view**: Side-by-side contract comparison

## 📝 Notes

- Reports are generated using OpenAI with web search
- Generation time: ~30-60 seconds per contract
- Reports are in the contract's original language
- Requires valid OPENAI_API_KEY in backend
- Internet connection required for AI and web search

---

**Status**: ✅ Fully implemented and ready for use!

