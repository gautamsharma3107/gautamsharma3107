# HackerRank Achievements Integration

This repository now includes automated HackerRank achievements integration that updates daily in the README.

## Features

### 🔄 Automated Updates
- **Daily Schedule**: Updates every day at 6:00 AM UTC
- **Manual Trigger**: Can be triggered manually from GitHub Actions tab
- **Auto-commit**: Automatically commits changes to the repository

### 🎨 Visual Elements
- **Profile Badge**: Direct link to HackerRank profile with official styling
- **Skills Badges**: Technology-specific badges for each skill domain
- **Certifications**: Display of earned HackerRank certificates
- **Statistics**: Rank, points, and solved challenges (when available)

### 🛠️ Technical Details

#### Files Structure
```
├── .github/workflows/update-hackerrank.yml  # GitHub Actions workflow
├── scripts/
│   ├── fetch_hackerrank.py                 # Data fetcher
│   └── update_readme.py                    # README updater
├── requirements.txt                        # Python dependencies
└── hackerrank_stats.md                    # Generated content
```

#### How It Works
1. **fetch_hackerrank.py** attempts to fetch real data from HackerRank profile
2. If the API is unavailable, it uses meaningful fallback data
3. **update_readme.py** integrates the generated content into README.md
4. GitHub Actions commits and pushes the changes automatically

#### Manual Execution
To run manually (for testing or immediate updates):

```bash
# Install dependencies
pip install -r requirements.txt

# Run the fetcher
cd scripts
python fetch_hackerrank.py

# Update README
python update_readme.py
```

### 🔧 Customization

#### Adding New Skills
Edit the `get_fallback_data()` function in `fetch_hackerrank.py` to add new skills:

```python
'badges': ['Problem Solving', 'Python', 'C++', 'Java', 'JavaScript'],
```

#### Changing Update Schedule
Modify the cron expression in `.github/workflows/update-hackerrank.yml`:

```yaml
schedule:
  - cron: '0 6 * * *'  # Daily at 6:00 AM UTC
```

#### Styling Badges
Badge colors and styles can be customized in the `generate_badges_markdown()` function.

## Troubleshooting

### Common Issues
1. **Network Access**: The script gracefully handles when HackerRank is not accessible
2. **API Limits**: Uses fallback data to ensure the section is always populated
3. **GitHub Actions**: Check the Actions tab for workflow execution logs

### Contributing
Feel free to enhance the fetching logic, add new visual elements, or improve the data parsing when HackerRank APIs become available.