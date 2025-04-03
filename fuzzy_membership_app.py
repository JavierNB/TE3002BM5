import streamlit as st
import numpy as np
import plotly.graph_objects as go

def validate_triangular(a, b, c):
    if not (a < b < c):
        st.error("Parameters must satisfy: a < b < c")
        return False
    return True

def validate_trapezoidal(a, b, c, d):
    if not (a < b < c < d):
        st.error("Parameters must satisfy: a < b < c < d")
        return False
    return True

def triangular_mf(x, a, b, c):
    return np.maximum(np.minimum((x - a)/(b - a), (c - x)/(c - b)), 0)

def gaussian_mf(x, mean, sigma):
    return np.exp(-((x - mean)**2)/(2*sigma**2))

def trapezoidal_mf(x, a, b, c, d):
    return np.maximum(np.minimum(np.minimum((x - a)/(b - a), 1), (d - x)/(d - c)), 0)

def bell_mf(x, a, b, c):
    return 1 / (1 + np.abs((x - c)/a)**(2*b))

def sigmoidal_mf(x, a, c):
    return 1 / (1 + np.exp(-a*(x - c)))

def main():
    st.title("Fuzzy Membership Functions Explorer")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Triangular", "Gaussian", "Trapezoidal", "Bell", "Sigmoidal"
    ])
    
    x = np.linspace(0, 10, 1000)
    
    with tab1:
        st.header("Triangular Membership Function")
        st.markdown(r"""
        **Equation:**
        $$
        \mu(x) = \begin{cases}
        0 & \text{if } x \leq a \\
        \frac{x - a}{b - a} & \text{if } a < x \leq b \\
        \frac{c - x}{c - b} & \text{if } b < x \leq c \\
        0 & \text{if } x > c
        \end{cases}
        $$
        """)
        col1, col2, col3 = st.columns(3)
        with col1: a = st.slider("a (Left)", 0.0, 10.0, 2.0, key="tri_a")
        with col2: b = st.slider("b (Peak)", 0.0, 10.0, 5.0, key="tri_b")
        with col3: c = st.slider("c (Right)", 0.0, 10.0, 8.0, key="tri_c")
        
        if validate_triangular(a, b, c):
            y = triangular_mf(x, a, b, c)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(width=3)))
            fig.update_layout(
                title="Triangular Membership Function",
                xaxis_range=[0, 10],
                yaxis_range=[0, 1.1]
            )
            st.plotly_chart(fig)
    
    with tab2:
        st.header("Gaussian Membership Function")
        st.markdown(r"""
        **Equation:**
        $$
        \mu(x) = e^{-\frac{(x - \text{mean})^2}{2\sigma^2}}
        $$
        """)
        col1, col2 = st.columns(2)
        with col1: mean = st.slider("Mean", 0.0, 10.0, 5.0, key="gauss_mean")
        with col2: sigma = st.slider("Sigma", 0.1, 5.0, 1.0, key="gauss_sigma")
        
        y = gaussian_mf(x, mean, sigma)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(width=3)))
        fig.update_layout(
            title="Gaussian Membership Function",
            yaxis_range=[0, 1.1]
        )
        st.plotly_chart(fig)
    
    with tab3:
        st.header("Trapezoidal Membership Function")
        st.markdown(r"""
        **Equation:**
        $$
        \mu(x) = \begin{cases}
        0 & \text{if } x \leq a \\
        \frac{x - a}{b - a} & \text{if } a < x \leq b \\
        1 & \text{if } b < x \leq c \\
        \frac{d - x}{d - c} & \text{if } c < x \leq d \\
        0 & \text{if } x > d
        \end{cases}
        $$
        """)
        col1, col2, col3, col4 = st.columns(4)
        with col1: a = st.slider("a (Left)", 0.0, 10.0, 2.0, key="trap_a")
        with col2: b = st.slider("b (Left Top)", a, 10.0, 4.0, key="trap_b")
        with col3: c = st.slider("c (Right Top)", b, 10.0, 6.0, key="trap_c")
        with col4: d = st.slider("d (Right)", c, 10.0, 8.0, key="trap_d")
        
        if validate_trapezoidal(a, b, c, d):
            y = trapezoidal_mf(x, a, b, c, d)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(width=3)))
            fig.update_layout(
                title="Trapezoidal Membership Function",
                yaxis_range=[0, 1.1]
            )
            st.plotly_chart(fig)
    
    with tab4:
        st.header("Generalized Bell Membership Function")
        st.markdown(r"""
        **Equation:**
        $$
        \mu(x) = \frac{1}{1 + \left|\frac{x - c}{a}\right|^{2b}}
        $$
        """)
        col1, col2, col3 = st.columns(3)
        with col1: a = st.slider("a (Width)", 0.1, 5.0, 1.0, key="bell_a")
        with col2: b = st.slider("b (Slope)", 0.1, 10.0, 2.0, key="bell_b")
        with col3: c = st.slider("c (Center)", 0.0, 10.0, 5.0, key="bell_c")
        
        y = bell_mf(x, a, b, c)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(width=3)))
        fig.update_layout(
            title="Generalized Bell Membership Function",
            yaxis_range=[0, 1.1]
        )
        st.plotly_chart(fig)
    
    with tab5:
        st.header("Sigmoidal Membership Function")
        st.markdown(r"""
        **Equation:**
        $$
        \mu(x) = \frac{1}{1 + e^{-a(x - c)}}
        $$
        """)
        col1, col2 = st.columns(2)
        with col1: a = st.slider("a (Slope)", 0.1, 5.0, 1.0, key="sig_a")
        with col2: c = st.slider("c (Inflection)", 0.0, 10.0, 5.0, key="sig_c")
        
        y = sigmoidal_mf(x, a, c)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(width=3)))
        fig.update_layout(
            title="Sigmoidal Membership Function",
            yaxis_range=[0, 1.1]
        )
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
