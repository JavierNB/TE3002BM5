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
        st.markdown(r"""### Explanation of the Triangular Membership Function

The **Triangular Membership Function** is a type of fuzzy logic function used to represent the degree of membership of a value $ x $ within a fuzzy set. This function is defined by three parameters: $ a $, $ b $, and $ c $. Here's a breakdown of its components:

#### Parameters:
- **$ a $**: The lower limit of the triangular function.
- **$ b $**: The peak (maximum) point of the triangle, where the membership degree is 1.
- **$ c $**: The upper limit of the triangular function.

#### Function Behavior:
1. **For** $ x \leq a $:
   - The membership degree $ \mu(x) = 0 $. This means that values less than or equal to $ a $ do not belong to the fuzzy set.

2. **For $ a < x \leq b $**:
   - The membership degree increases linearly from 0 to 1. It is calculated as:
     $$
     \mu(x) = \frac{x - a}{b - a}
     $$
   - As $ x $ approaches $ b $, $ \mu(x) $ approaches 1, indicating full membership.

3. **For $ b < x \leq c $**:
   - The membership degree decreases linearly from 1 to 0. It is calculated as:
     $$
     \mu(x) = \frac{c - x}{c - b}
     $$
   - As $ x $ approaches $ c $, $ \mu(x) $ approaches 0, indicating no membership.

4. **For $ x > c $**:
   - The membership degree $ \mu(x) = 0 $. Values greater than $ c $ do not belong to the fuzzy set.
        """)
    
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
        st.markdown(r"""### Explanation of the Gaussian Membership Function
The **Gaussian Membership Function** is a commonly used function in fuzzy logic and statistics to represent the degree of membership of a value $ x $ within a fuzzy set. It is characterized by a bell-shaped curve and is defined by two parameters: the mean and the standard deviation.

#### Parameters:
- **Mean ($ \text{mean} $)**: The center of the Gaussian curve, indicating the point of maximum membership (where the membership degree is 1).
- **Standard Deviation ($ \sigma $)**: Determines the width of the curve. A smaller $ \sigma $ results in a steeper curve, while a larger $ \sigma $ creates a flatter curve.

#### Function Behavior:
1. **At the Mean**:
   - When $ x $ is equal to the mean, the membership degree is at its maximum:
     $$
     \mu(\text{mean}) = e^{0} = 1
     $$

2. **As $ x $ Moves Away from the Mean**:
   - The membership degree decreases exponentially as $ x $ moves away from the mean. This is governed by the equation:
     $$
     \mu(x) = e^{-\frac{(x - \text{mean})^2}{2\sigma^2}}
     $$
   - As $ |x - \text{mean}| $ increases, $ \mu(x) $ approaches 0, indicating lower membership.

3. **Shape of the Curve**:
   - The Gaussian function produces a symmetric bell-shaped curve. The area under the curve represents the total membership, which integrates to 1 over the entire range.
                    """)
    
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
            st.markdown(r"""### Explanation of the Trapezoidal Membership Function

The **Trapezoidal Membership Function** is a type of fuzzy membership function that is used to represent the degree of membership of a value $ x $ within a fuzzy set. It is particularly useful in situations where the membership grades need to be defined over an interval, allowing for a flat top section. 

#### Parameters:
- **$ a $**: The lower limit where the membership starts increasing.
- **$ b $**: The point where the membership reaches its maximum (1).
- **$ c $**: The point where the membership remains at its maximum (1) until it starts to decrease.
- **$ d $**: The upper limit where the membership starts decreasing to 0.

#### Function Behavior:
1. **For $ x \leq a $**:
   - The membership degree is $ \mu(x) = 0 $. Values less than or equal to $ a $ do not belong to the fuzzy set.

2. **For $ a < x \leq b $**:
   - The membership degree increases linearly from 0 to 1:
     $$
     \mu(x) = \frac{x - a}{b - a}
     $$
   - As $ x $ approaches $ b $, the membership degree reaches its maximum of 1.

3. **For $ b < x \leq c $**:
   - The membership degree remains constant at 1, indicating full membership in the fuzzy set.

4. **For $ c < x \leq d $**:
   - The membership degree decreases linearly from 1 to 0:
     $$
     \mu(x) = \frac{d - x}{d - c}
     $$
   - As $ x $ approaches $ d $, the membership degree approaches 0.

5. **For $ x > d $**:
   - The membership degree is $ \mu(x) = 0 $. Values greater than $ d $ do not belong to the fuzzy set.

### Visual Representation
The trapezoidal shape allows for a clear representation of the membership function, with a flat top that indicates a range of values that fully belong to the fuzzy set.
""")
    
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
        st.markdown(r"""### Explanation of the Generalized Bell Membership Function
        
The Generalized Bell Membership Function is a type of fuzzy membership function used in fuzzy logic systems to define the degree of membership of a value $x$ within a fuzzy set. This function is characterized by its bell-shaped curve, which can be adjusted to fit various applications.
$$
\mu(x) = \frac{1}{1 + \left|\frac{x - c}{a}\right|^{2b}}
$$
The equation consists of three parameters: $a$, $b$, and $c$. Here's a breakdown of its components:

Where:

- **$\mu(x)$**: The degree of membership of the input value $x$ in the fuzzy set.
- **$c$**: The center of the bell-shaped curve, which represents the point of maximum membership (typically 1).
- **$a$**: The scale parameter that affects the width of the bell curve. A larger $a$ value results in a wider curve.
- **$b$**: The shape parameter that controls the sharpness of the curve. A higher $b$ value leads to a steeper decline in membership degree.

The Generalized Bell Membership Function is a versatile tool in fuzzy logic, as it allows for flexible modeling of fuzzy sets by adjusting the $a$ and $b$ parameters. This function is commonly used in various applications, such as artificial intelligence, control systems, and decision-making processes, where the representation of gradual membership is important.
                    """)
    
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
        st.markdown(r"""### Explanation of the Sigmoidal Membership Function
The Sigmoidal Membership Function is another type of fuzzy membership function used in fuzzy logic systems. It is characterized by a smooth, S-shaped curve that represents the degree of membership of an input value x within a fuzzy set.

The key aspects of the Sigmoidal Membership Function are:

1. **Equation**:
   The mathematical expression for the Sigmoidal Membership Function is:
   $$
   \mu(x) = \frac{1}{1 + e^{-a(x - c)}}
   $$

2. **Parameters**:
   - **$c$**: This parameter represents the center or inflection point of the sigmoidal curve, where the membership degree is 0.5.
   - **$a$**: This parameter controls the steepness of the curve. A larger value of $a$ results in a sharper transition between low and high membership degrees, while a smaller value of $a$ leads to a more gradual transition.

The Sigmoidal Membership Function is often used in situations where a gradual transition between membership and non-membership is desired. It is particularly useful in applications where the input values can be categorized into two distinct groups, such as "low" and "high", with a smooth transition between them.

Some key properties of the Sigmoidal Membership Function:

- The function is bounded between 0 and 1, representing the range of possible membership degrees.
- The curve is monotonically increasing, meaning it steadily rises from 0 to 1 as the input value x increases.
- The inflection point at $x = c$ represents the point where the membership degree is 0.5, serving as the decision boundary between membership and non-membership.
- The steepness of the curve, controlled by the $a$ parameter, determines how quickly the membership degree transitions from 0 to 1 around the inflection point.
                    """)

if __name__ == "__main__":
    main()
