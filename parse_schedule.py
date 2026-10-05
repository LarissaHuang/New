import pandas as pd
import re

# load the master schedule 
df = pd.read_csv('All Sets Schedule MLTS.csv', header=None)

# Map sets to their respective column indices across Mon-Fri
sets_mapping = {
    'Set_A': [1, 5, 9, 13, 17],
    'Set_B': [2, 6, 10, 14, 18],
    'Set_C': [3, 7, 11, 15, 19],
    'Set_D': [4, 8, 12, 16, 20]
}

# google calendar colours by their number code, to make things pretty:
def get_color_id(course_text):
    text = course_text.upper()
    if 'BHSC1139' in text:
        return '9' # blueberry 
    elif 'BHSC1310' in text:
        return '7' # peacock 
    elif 'MLSC1218' in text:
        return '2' # sage
    elif 'MLSC1309' in text:
        return '3' # grape
    elif 'MLSC1314' in text:
        return '5' # banana 
    elif 'COMM1370' in text:
        return '6' # tangerine 
    else:
        return '1' # lavender (holidays, school closures)

# function to identify shared school-wide/admin events
def is_shared_event(text):
    t = text.lower()
    keywords = ['no classes', 'orientation', 'truth and reconciliation', 'thanksgiving', 'remembrance day', 'final exams', 'holiday']
    return any(k in t for k in keywords)

# process each set independently
for set_name, cols in sets_mapping.items():
    events = []
    current_date = None
    
    # iterate through weekly blocks (11 rows per week)
    for start_row in range(0, len(df), 11):
        day_cols_map = {0: cols[0], 1: cols[1], 2: cols[2], 3: cols[3], 4: cols[4]}
        set_a_cols_map = {0: 1, 1: 5, 2: 9, 3: 13, 4: 17}
        
        # extract calendar dates for Monday through Friday of the current week, skipping Saturday and Sunday
        dates = {}
        for day_idx, c in day_cols_map.items():
            date_col_idx = 1 + (day_idx * 4)
            d_val = df.iloc[start_row, date_col_idx]
            if pd.notna(d_val) and '/' in str(d_val):
                current_date = str(d_val).strip()
            dates[day_idx] = current_date
            
        # parse time rows within the week block
        for r in range(start_row + 3, min(start_row + 11, len(df))):
            time_val = str(df.iloc[r, 0]).strip()
            if '-' in time_val and ':' in time_val:
                try:
                    start_t, end_t = [t.strip() for t in time_val.split('-')]
                except:
                    continue
                
                for day_idx, c in day_cols_map.items():
                    cell_content = str(df.iloc[r, c]).strip()
                    
                    # if this set's cell is empty, check if Set A has a shared school-wide event
                    # BCIT has by default populated these administrative events in Set A's schedule
                    if (not cell_content or cell_content == 'nan') and set_name != 'Set_A':
                        set_a_col = set_a_cols_map[day_idx]
                        set_a_content = str(df.iloc[r, set_a_col]).strip()
                        if set_a_content and set_a_content != 'nan':
                            if is_shared_event(set_a_content):
                                cell_content = set_a_content
                    
                    if cell_content and cell_content != 'nan':
                        date_str = dates.get(day_idx)
                        if not date_str:
                            continue
                            
                        for line in cell_content.split('\n'):
                            line = line.strip()
                            if line:
                                parts = line.split()
                                subject = " ".join(parts[:2]) if len(parts) >= 2 else line
                                color = get_color_id(subject)
                                
                                # Extract room location pattern (e.g., SW03 1710)
                                location = ""
                                loc_match = re.search(r'([A-Z0-9]+\s+[A-Z0-9]+)', line)
                                if loc_match:
                                    location = loc_match.group(1)
                                    
                                events.append({
                                    'Subject': subject,
                                    'Start Date': date_str,
                                    'Start Time': start_t,
                                    'End Date': date_str,
                                    'End Time': end_t,
                                    'Description': line,
                                    'Location': location,
                                    'Color ID': color
                                })
                                
    # export individual CSV for each set 
    out_df = pd.DataFrame(events).drop_duplicates(subset=['Start Date', 'Start Time', 'Description'])
    filename = f'google_calendar_{set_name}.csv'
    out_df.to_csv(filename, index=False)
    print(f"Successfully generated {filename} with {len(out_df)} events!")