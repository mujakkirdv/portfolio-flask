# app.py - Enhanced for Python 3.12.0 with 3D designs on every page (PythonAnywhere Ready)
from flask import Flask, render_template, request, jsonify
import plotly.graph_objs as go
import plotly.express as px
import plotly.io as pio
import pandas as pd
import numpy as np
from scipy import stats
import json
import os

app = Flask(__name__)

# Set random seed for reproducibility
np.random.seed(42)

# Generate comprehensive sample data
def generate_sample_data():
    """Generate sample data for analytics"""
    # Time series data
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Sales data with seasonal pattern
    seasonal_pattern = [0.8, 0.7, 0.9, 1.0, 1.1, 1.2, 1.15, 1.1, 1.05, 1.1, 1.2, 1.3]
    base_sales = 100000
    monthly_sales = base_sales * np.array(seasonal_pattern) + np.random.normal(0, 5000, 12)
    monthly_profit = monthly_sales * np.random.uniform(0.15, 0.25, 12)
    
    # Customer data
    n_customers = 500
    customer_ages = np.random.randint(18, 70, n_customers)
    customer_income = np.random.normal(50000, 20000, n_customers)
    customer_spending = 500 + (customer_ages * 10) + (customer_income / 1000) + np.random.normal(0, 200, n_customers)
    
    # Product data
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E', 'Product F']
    product_sales = np.random.randint(100, 800, len(products))
    product_profit_margin = np.random.uniform(0.1, 0.45, len(products))
    product_customer_satisfaction = np.random.uniform(3.5, 5.0, len(products))
    
    # Geographic data
    regions = ['North', 'South', 'East', 'West', 'Central']
    region_sales = np.random.randint(50000, 200000, len(regions))
    region_growth = np.random.uniform(-0.05, 0.15, len(regions))
    
    return {
        'months': months,
        'monthly_sales': monthly_sales,
        'monthly_profit': monthly_profit,
        'customer_ages': customer_ages,
        'customer_income': customer_income,
        'customer_spending': customer_spending,
        'products': products,
        'product_sales': product_sales,
        'product_profit_margin': product_profit_margin,
        'product_customer_satisfaction': product_customer_satisfaction,
        'regions': regions,
        'region_sales': region_sales,
        'region_growth': region_growth
    }

data = generate_sample_data()

@app.route('/')
def home():
    """Home page with 3D analytics dashboard"""
    
    # 1. 3D Surface Plot - Sales Performance Matrix
    x = np.linspace(0, 10, 30)
    y = np.linspace(0, 10, 30)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X) * np.cos(Y * 1.5) * 100 + np.random.normal(0, 8, (30, 30))
    
    surface_3d = go.Figure(data=[go.Surface(
        z=Z, 
        x=x, 
        y=y, 
        colorscale='Viridis',
        contours=dict(
            z=dict(show=True, usecolormap=True, highlightcolor="limegreen", project=dict(z=True))
        )
    )])
    surface_3d.update_layout(
        title={
            'text': '3D Sales Performance Surface: Marketing vs Engagement Impact',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Marketing Spend ($K)',
            yaxis_title='Customer Engagement Score',
            zaxis_title='Sales Performance ($K)',
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.5)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    surface_chart = pio.to_html(surface_3d, full_html=False, config={'responsive': True})
    
    # 2. 3D Scatter Plot - Customer Segmentation
    n_points = 200
    age = data['customer_ages'][:n_points]
    income = data['customer_income'][:n_points]
    spending = data['customer_spending'][:n_points]
    
    scatter_3d = go.Figure(data=[go.Scatter3d(
        x=age,
        y=income,
        z=spending,
        mode='markers',
        marker=dict(
            size=6,
            color=spending,
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title='Spending Score', x=0, y=0.5),
            opacity=0.7
        ),
        text=[f'Age: {a}<br>Income: ${i:,.0f}<br>Spending: ${s:,.0f}' 
              for a, i, s in zip(age, income, spending)],
        hovertemplate='<b>Customer #{pointNumber}</b><br>%{text}<extra></extra>'
    )])
    scatter_3d.update_layout(
        title={
            'text': '3D Customer Segmentation: Age vs Income vs Spending',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Age (Years)',
            yaxis_title='Annual Income ($)',
            zaxis_title='Annual Spending ($)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    scatter_3d_chart = pio.to_html(scatter_3d, full_html=False, config={'responsive': True})
    
    # 3. 3D Mesh Plot - Product Performance
    product_x = np.array([1, 2, 3, 4, 5, 6])
    product_y = data['product_profit_margin'] * 100
    product_z = data['product_customer_satisfaction']
    
    mesh_3d = go.Figure(data=[go.Scatter3d(
        x=product_x,
        y=product_y,
        z=product_z,
        mode='markers+lines',
        marker=dict(
            size=[s / 50 for s in data['product_sales']],
            color=data['product_sales'],
            colorscale='Hot',
            showscale=True,
            colorbar=dict(title='Sales Volume'),
            sizemode='diameter',
            sizeref=8
        ),
        line=dict(color='cyan', width=2),
        text=[f'Product: {p}<br>Sales: {s}<br>Margin: {m:.1f}%<br>Satis: {sat:.1f}' 
              for p, s, m, sat in zip(data['products'], data['product_sales'], 
                                      data['product_profit_margin'] * 100, 
                                      data['product_customer_satisfaction'])],
        hovertemplate='%{text}<extra></extra>'
    )])
    mesh_3d.update_layout(
        title={
            'text': '3D Product Performance Matrix',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Product Index',
            yaxis_title='Profit Margin (%)',
            zaxis_title='Customer Satisfaction (1-5)',
            camera=dict(eye=dict(x=1.2, y=1.2, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    mesh_3d_chart = pio.to_html(mesh_3d, full_html=False, config={'responsive': True})
    
    return render_template('home.html', 
                         surface_chart=surface_chart,
                         scatter_3d_chart=scatter_3d_chart,
                         mesh_3d_chart=mesh_3d_chart)

@app.route('/about')
def about():
    """About page with 3D skill visualization"""
    
    # 1. 3D Bar Chart - Skills Proficiency
    skills = ['Python', 'SQL', 'Pandas', 'NumPy', 'Plotly', 'ML', 'Power BI', 'Tableau']
    proficiency = [92, 88, 90, 87, 85, 78, 82, 80]
    
    # Create 3D bars using Scatter3d
    skill_3d = go.Figure()
    
    for i, (skill, prof) in enumerate(zip(skills, proficiency)):
        skill_3d.add_trace(go.Scatter3d(
            x=[i, i],
            y=[0, prof],
            z=[0, 0],
            mode='lines',
            line=dict(color='cyan', width=8),
            showlegend=False,
            hoverinfo='none'
        ))
        
        skill_3d.add_trace(go.Scatter3d(
            x=[i],
            y=[prof],
            z=[0],
            mode='markers',
            marker=dict(size=10, color='yellow'),
            name=skill,
            text=f'{skill}: {prof}%',
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
    
    skill_3d.update_layout(
        title={
            'text': '3D Technical Skills Proficiency',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis=dict(title='Skills', ticktext=skills, tickvals=list(range(len(skills))), tickangle=45),
            yaxis=dict(title='Proficiency (%)', range=[0, 100]),
            zaxis=dict(title='', visible=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    skills_3d_chart = pio.to_html(skill_3d, full_html=False, config={'responsive': True})
    
    # 2. 3D Sphere Plot - Experience Distribution
    years_exp = np.random.normal(3, 1.5, 100)
    projects_completed = np.random.poisson(8, 100)
    impact_score = years_exp * 10 + projects_completed * 2 + np.random.normal(0, 5, 100)
    
    experience_3d = go.Figure(data=[go.Scatter3d(
        x=years_exp,
        y=projects_completed,
        z=impact_score,
        mode='markers',
        marker=dict(
            size=8,
            color=impact_score,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Impact Score'),
            opacity=0.8
        ),
        text=[f'Experience: {y:.1f} years<br>Projects: {p}<br>Impact: {i:.1f}' 
              for y, p, i in zip(years_exp, projects_completed, impact_score)],
        hovertemplate='%{text}<extra></extra>'
    )])
    experience_3d.update_layout(
        title={
            'text': '3D Experience Impact Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Years of Experience',
            yaxis_title='Projects Completed',
            zaxis_title='Impact Score',
            camera=dict(eye=dict(x=1.2, y=1.2, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    experience_3d_chart = pio.to_html(experience_3d, full_html=False, config={'responsive': True})
    
    # 3. 3D Surface - Career Growth Trajectory
    career_years = np.arange(0, 10, 0.5)
    skill_growth = 50 * (1 - np.exp(-career_years / 3)) + np.random.normal(0, 2, len(career_years))
    responsibility_growth = 40 * (1 - np.exp(-career_years / 4)) + np.random.normal(0, 2, len(career_years))
    
    growth_3d = go.Figure(data=[go.Scatter3d(
        x=career_years,
        y=skill_growth,
        z=responsibility_growth,
        mode='lines+markers',
        marker=dict(size=5, color='red', colorscale='Hot'),
        line=dict(width=3, color='cyan'),
        text=[f'Year: {y:.1f}<br>Skills: {s:.1f}%<br>Responsibility: {r:.1f}%' 
              for y, s, r in zip(career_years, skill_growth, responsibility_growth)],
        hovertemplate='%{text}<extra></extra>'
    )])
    growth_3d.update_layout(
        title={
            'text': '3D Career Growth Trajectory',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Years',
            yaxis_title='Skill Development (%)',
            zaxis_title='Responsibility Level (%)',
            camera=dict(eye=dict(x=1.5, y=1.2, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    growth_3d_chart = pio.to_html(growth_3d, full_html=False, config={'responsive': True})
    
    return render_template('about.html', 
                         skills_3d_chart=skills_3d_chart,
                         experience_3d_chart=experience_3d_chart,
                         growth_3d_chart=growth_3d_chart)

@app.route('/projects')
def projects():
    """Projects page with 3D project analytics"""
    
    # 1. 3D Project Performance Matrix
    project_names = ['Sales Dashboard', 'Financial Analysis', 'Customer Analytics', 
                     'Transaction System', 'AI Dashboard', 'Inventory Management']
    complexity = [85, 70, 95, 65, 90, 75]
    impact = [88, 82, 92, 70, 85, 78]
    lines_of_code = [2500, 1800, 3200, 1500, 2800, 2100]
    
    project_3d = go.Figure(data=[go.Scatter3d(
        x=complexity,
        y=impact,
        z=lines_of_code,
        mode='markers+text',
        marker=dict(
            size=15,
            color=impact,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Impact Score'),
            symbol='circle',
            opacity=0.8
        ),
        text=project_names,
        textposition='top center',
        textfont=dict(size=10, color='white'),
        hovertemplate='<b>%{text}</b><br>Complexity: %{x}<br>Impact: %{y}<br>LOC: %{z:,}<extra></extra>'
    )])
    project_3d.update_layout(
        title={
            'text': '3D Project Performance Matrix',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Complexity Score',
            yaxis_title='Business Impact Score',
            zaxis_title='Lines of Code',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    project_performance_3d = pio.to_html(project_3d, full_html=False, config={'responsive': True})
    
    # 2. 3D Technology Stack Distribution
    technologies = ['Python', 'Flask', 'Plotly', 'Pandas', 'SQL', 'JavaScript']
    usage_frequency = [95, 80, 85, 90, 75, 70]
    proficiency = [92, 85, 88, 90, 82, 78]
    
    tech_3d = go.Figure(data=[go.Scatter3d(
        x=list(range(len(technologies))),
        y=usage_frequency,
        z=proficiency,
        mode='markers+lines',
        marker=dict(
            size=12,
            color=usage_frequency,
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title='Usage (%)'),
            symbol='diamond'
        ),
        line=dict(color='cyan', width=2),
        text=[f'{tech}<br>Usage: {u}%<br>Proficiency: {p}%' 
              for tech, u, p in zip(technologies, usage_frequency, proficiency)],
        hovertemplate='%{text}<extra></extra>'
    )])
    tech_3d.update_layout(
        title={
            'text': '3D Technology Stack Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis=dict(title='Technologies', ticktext=technologies, tickvals=list(range(len(technologies))), tickangle=45),
            yaxis=dict(title='Usage Frequency (%)', range=[0, 100]),
            zaxis=dict(title='Proficiency Level (%)', range=[0, 100]),
            camera=dict(eye=dict(x=1.2, y=1.2, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    tech_stack_3d = pio.to_html(tech_3d, full_html=False, config={'responsive': True})
    
    # 3. 3D Timeline of Projects
    project_durations = [3, 2.5, 4, 2, 3.5, 2.8]
    team_size = [2, 1, 3, 1, 2, 2]
    roi = [150, 180, 220, 120, 200, 160]
    
    timeline_3d = go.Figure(data=[go.Scatter3d(
        x=project_durations,
        y=team_size,
        z=roi,
        mode='markers+lines',
        marker=dict(
            size=20,
            color=roi,
            colorscale='Hot',
            showscale=True,
            colorbar=dict(title='ROI (%)'),
            symbol='circle-open'
        ),
        line=dict(color='yellow', width=3),
        text=project_names,
        textposition='top center',
        hovertemplate='<b>%{text}</b><br>Duration: %{x} months<br>Team Size: %{y}<br>ROI: %{z}%<extra></extra>'
    )])
    timeline_3d.update_layout(
        title={
            'text': '3D Project Timeline & ROI Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Project Duration (Months)',
            yaxis_title='Team Size',
            zaxis_title='Return on Investment (%)',
            camera=dict(eye=dict(x=1.8, y=1.8, z=1.5)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    timeline_3d_chart = pio.to_html(timeline_3d, full_html=False, config={'responsive': True})
    
    return render_template('projects.html', 
                         project_performance_3d=project_performance_3d,
                         tech_stack_3d=tech_stack_3d,
                         timeline_3d_chart=timeline_3d_chart)

@app.route('/contact')
def contact():
    """Contact page with 3D network visualization"""
    
    # 1. 3D Network Graph - Professional Network
    np.random.seed(42)
    n_nodes = 20
    positions = np.random.randn(n_nodes, 3) * 2
    
    # Create connections (random edges)
    edges = []
    for i in range(n_nodes):
        for j in range(i+1, n_nodes):
            if np.random.random() < 0.15:  # 15% connection probability
                edges.append((i, j))
    
    network_3d = go.Figure()
    
    # Add nodes
    network_3d.add_trace(go.Scatter3d(
        x=positions[:, 0],
        y=positions[:, 1],
        z=positions[:, 2],
        mode='markers+text',
        marker=dict(
            size=12,
            color='lightblue',
            symbol='circle',
            line=dict(color='white', width=1)
        ),
        text=[f'Node {i}' for i in range(n_nodes)],
        textposition='top center',
        hovertemplate='<b>Connection Point</b><extra></extra>'
    ))
    
    # Add edges
    for edge in edges:
        network_3d.add_trace(go.Scatter3d(
            x=[positions[edge[0], 0], positions[edge[1], 0]],
            y=[positions[edge[0], 1], positions[edge[1], 1]],
            z=[positions[edge[0], 2], positions[edge[1], 2]],
            mode='lines',
            line=dict(color='rgba(100, 100, 255, 0.5)', width=1),
            showlegend=False,
            hoverinfo='none'
        ))
    
    network_3d.update_layout(
        title={
            'text': '3D Professional Network Visualization',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis=dict(title='', visible=False),
            yaxis=dict(title='', visible=False),
            zaxis=dict(title='', visible=False),
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600,
        showlegend=False
    )
    network_3d_chart = pio.to_html(network_3d, full_html=False, config={'responsive': True})
    
    # 2. 3D Cone Plot - Communication Channels
    channels = ['Email', 'Phone', 'LinkedIn', 'GitHub', 'Portfolio', 'Conference']
    frequency = [85, 60, 75, 70, 65, 40]
    engagement = [90, 75, 85, 80, 88, 70]
    
    cone_3d = go.Figure(data=[go.Scatter3d(
        x=list(range(len(channels))),
        y=frequency,
        z=engagement,
        mode='markers',
        marker=dict(
            size=20,
            color=engagement,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title='Engagement Score'),
            symbol='circle',
            sizemode='diameter',
            sizeref=2
        ),
        text=[f'{ch}<br>Frequency: {f}%<br>Engagement: {e}%' 
              for ch, f, e in zip(channels, frequency, engagement)],
        hovertemplate='%{text}<extra></extra>'
    )])
    cone_3d.update_layout(
        title={
            'text': '3D Communication Channel Analysis',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis=dict(title='Communication Channels', ticktext=channels, tickvals=list(range(len(channels))), tickangle=45),
            yaxis=dict(title='Usage Frequency (%)', range=[0, 100]),
            zaxis=dict(title='Engagement Score', range=[0, 100]),
            camera=dict(eye=dict(x=1.2, y=1.2, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    cone_3d_chart = pio.to_html(cone_3d, full_html=False, config={'responsive': True})
    
    # 3. 3D Geographic Reach
    cities = ['Dhaka', 'Chittagong', 'Sylhet', 'Rajshahi', 'Khulna', 'Barisal']
    lat = [23.8103, 22.3569, 24.8949, 24.3745, 22.8456, 22.7010]
    lon = [90.4125, 91.7832, 91.8736, 88.6042, 89.5403, 90.3535]
    activity = np.random.randint(50, 100, len(cities))
    
    geo_3d = go.Figure(data=[go.Scatter3d(
        x=lat,
        y=lon,
        z=activity,
        mode='markers',
        marker=dict(
            size=[a / 3 for a in activity],
            color=activity,
            colorscale='Hot',
            showscale=True,
            colorbar=dict(title='Activity Level'),
            symbol='circle'
        ),
        text=[f'{city}<br>Activity: {a}%' for city, a in zip(cities, activity)],
        hovertemplate='%{text}<extra></extra>'
    )])
    geo_3d.update_layout(
        title={
            'text': '3D Geographic Reach & Engagement',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'white'}
        },
        scene=dict(
            xaxis_title='Latitude',
            yaxis_title='Longitude',
            zaxis_title='Activity Level (%)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=600
    )
    geo_3d_chart = pio.to_html(geo_3d, full_html=False, config={'responsive': True})
    
    return render_template('contact.html', 
                         network_3d_chart=network_3d_chart,
                         cone_3d_chart=cone_3d_chart,
                         geo_3d_chart=geo_3d_chart)

# ============ IMPORTANT: PythonAnywhere Configuration ============
# This line is CRITICAL for PythonAnywhere deployment
application = app

if __name__ == '__main__':
    app.run(debug=True, port=5000)