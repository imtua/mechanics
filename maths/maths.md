# Mechanics equations

All simulations use the Euler-Lagrange equations

$$
\frac{d}{dt}\left(\frac{\partial L}{\partial \dot q_i}\right)-\frac{\partial L}{\partial q_i}=0,
\qquad L=T-V.
$$

The equations below use the same generalized coordinates and parameters as the simulator models.

## 1. Simple pendulum

Generalized coordinate: $q=\theta$.

The bob position relative to the pivot is

$$
\mathbf r=(l\sin\theta,-l\cos\theta).
$$

Kinetic and potential energies, up to an irrelevant additive constant in $V$, are

$$
T=\frac12 m l^2\dot\theta^2,
\qquad
V=mgl(1-\cos\theta).
$$

Therefore,

$$
ml^2\ddot\theta+mgl\sin\theta=0,
$$

or

$$
\ddot\theta+\frac{g}{l}\sin\theta=0.
$$

## 2. Double pendulum

Generalized coordinates: $q_1=\theta_1$ and $q_2=\theta_2$. The angles are measured from the downward vertical.

The bob positions are

$$
\mathbf r_1=(l_1\sin\theta_1,-l_1\cos\theta_1),
$$

$$
\mathbf r_2=(l_1\sin\theta_1+l_2\sin\theta_2,
-l_1\cos\theta_1-l_2\cos\theta_2).
$$

The energies are

$$
T=\frac12(m_1+m_2)l_1^2\dot\theta_1^2
+\frac12m_2l_2^2\dot\theta_2^2
+m_2l_1l_2\dot\theta_1\dot\theta_2\cos(\theta_1-\theta_2),
$$

$$
V=-(m_1+m_2)gl_1\cos\theta_1-m_2gl_2\cos\theta_2.
$$

The two equations of motion are

$$
(m_1+m_2)l_1^2\ddot\theta_1
+m_2l_1l_2\cos(\theta_1-\theta_2)\ddot\theta_2
+m_2l_1l_2\sin(\theta_1-\theta_2)\dot\theta_2^2
+(m_1+m_2)gl_1\sin\theta_1=0,
$$

$$
 m_2l_2^2\ddot\theta_2
+m_2l_1l_2\cos(\theta_1-\theta_2)\ddot\theta_1
-m_2l_1l_2\sin(\theta_1-\theta_2)\dot\theta_1^2
+m_2gl_2\sin\theta_2=0.
$$

## 3. Swinging Atwood machine

Generalized coordinates: $q_1=r$ and $q_2=\theta$.

The vertically constrained mass has height $r$. The swinging mass has position relative to its pivot

$$
\mathbf r_2=(r\sin\theta,-r\cos\theta).
$$

The energies are

$$
T=\frac12(M+m)\dot r^2+\frac12mr^2\dot\theta^2,
$$

$$
V=Mgr-mgr\cos\theta.
$$

The equations of motion are

$$
(M+m)\ddot r-mr\dot\theta^2+g(M-m\cos\theta)=0,
$$

$$
mr^2\ddot\theta+2mr\dot r\dot\theta+mgr\sin\theta=0.
$$

## 4. Cart and pendulum

Generalized coordinates: $q_1=x$ and $q_2=\theta$.

The pendulum bob position is

$$
\mathbf r=(x-l\sin\theta,\tfrac12-l\cos\theta).
$$

The spring has unstretched length $d$ and is attached to the cart so that its extension is $x$. Thus,

$$
V_{\text{spring}}=\frac12kx^2.
$$

The energies are

$$
T=\frac12(M+m)\dot x^2
-ml\cos\theta\dot x\dot\theta
+\frac12ml^2\dot\theta^2,
$$

$$
V=mg\left(\frac12-l\cos\theta\right)+\frac12kx^2.
$$

The equations of motion are

$$
(M+m)\ddot x-ml\cos\theta\ddot\theta
+ml\sin\theta\dot\theta^2+kx=0,
$$

$$
ml^2\ddot\theta-ml\cos\theta\ddot x+mgl\sin\theta=0.
$$

## 5. Rolling disk pendulum

Generalized coordinates:

$$
q=(x,\theta_1,\theta_2).
$$

The model contains a large ring, a disk rolling inside the ring, and a pendulum attached to the disk. Define

$$
R_m=\frac{R_o+R_i}{2},
\qquad
h=\frac{14}{25}R_o,
\qquad
\alpha=\frac{x}{R_o}.
$$

The ring center and center of mass are

$$
\mathbf c=(\hat{\mathbf p}x,\hat{\mathbf n}R_o/2),
\qquad
\mathbf c_M=\mathbf c-\frac{14}{25}R_o\,\hat{\mathbf y},
$$

where the simulator uses the normalized slope direction and its perpendicular normal. The rolling disk center is

$$
\mathbf c_r=\mathbf c+(R_i-r)\,(
\sin\theta_1,-\cos\theta_1),
$$

and the two pendulum masses are

$$
\mathbf c_{p\pm}=\mathbf c_r+
\left(\pm\frac{w_p}{2},-l_p\right)\text{ rotated by }-\theta_2.
$$

The angular velocities used by the model are

$$
\omega_M=\frac{\dot x}{R_o},
\qquad
\omega_r=\frac{\dot x}{R_o}+\frac{R_i-r}{r}\left(\dot\theta_1+\frac{\dot x}{R_o}\right),
\qquad
\omega_p=\dot\theta_2.
$$

The kinetic energy is

$$
T=\frac12M\lVert\dot{\mathbf c}_M\rVert^2
+\frac12I_m\omega_M^2
+\frac12m_r\lVert\dot{\mathbf c}_r\rVert^2
+\frac12I_r\omega_r^2
+\frac12m_p\left(\lVert\dot{\mathbf c}_{p+}\rVert^2+\lVert\dot{\mathbf c}_{p-}\rVert^2\right).
$$

For a spring between points $\mathbf a$ and $\mathbf b$ with natural length $l_0$ and stiffness $k$, the potential is

$$
V_s(\mathbf a,\mathbf b)=\frac12k\left(\lVert\mathbf b-\mathbf a\rVert-l_0\right)^2.
$$

The total potential energy is

$$
V=Mg(c_M)_y+ m_rg(c_r)_y
+m_pg\left((c_{p+})_y+(c_{p-})_y\right)
+V_{s1}+V_{s2}+V_{s3},
$$

where

$$
V_{s1}=V_s(\mathbf a_1,\mathbf b_1),
\quad
V_{s2}=V_s(\mathbf a_2,\mathbf b_2),
\quad
V_{s3}=V_s(\mathbf a_3,\mathbf c_r),
$$

with natural lengths $l_1,l_1,l_2$ and stiffnesses $k,k,k_2$. The three equations of motion are therefore

$$
\frac{d}{dt}\frac{\partial (T-V)}{\partial\dot x}
-\frac{\partial (T-V)}{\partial x}=0,
$$

$$
\frac{d}{dt}\frac{\partial (T-V)}{\partial\dot\theta_1}
-\frac{\partial (T-V)}{\partial\theta_1}=0,
$$

$$
\frac{d}{dt}\frac{\partial (T-V)}{\partial\dot\theta_2}
-\frac{\partial (T-V)}{\partial\theta_2}=0.
$$

These are the coupled equations expanded and integrated by the simulator.

## 6. Disk on slope

Generalized coordinate: $q=x$.

Let the slope direction be

$$
\hat{\mathbf p}=\frac{(2,-1)}{\sqrt5},
$$

with perpendicular normal

$$
\hat{\mathbf n}=\frac{(1,2)}{\sqrt5}.
$$

The disk center is

$$
\mathbf c=r\hat{\mathbf n}+x\hat{\mathbf p},
$$

and rolling without slipping gives

$$
\omega=\frac{\dot x}{r}.
$$

The energies are

$$
T=\frac12m\dot x^2+\frac12I\left(\frac{\dot x}{r}\right)^2
=\frac12\left(m+\frac{I}{r^2}\right)\dot x^2,
$$

$$
V=mg\left(\frac{2r-x}{\sqrt5}\right).
$$

The equation of motion is

$$
\left(m+\frac{I}{r^2}\right)\ddot x-\frac{mg}{\sqrt5}=0.
$$

Equivalently,

$$
\ddot x=\frac{mg}{\sqrt5\left(m+I/r^2\right)}.
$$
