import numpy as np
from matplotlib.animation import FuncAnimation
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import math 
import time 
from st_pages import Page, show_pages, add_page_title, hide_pages
from constants import pages_created
import base64
import os

class BayesianRegularization():
    def __init__(self, slider_nsd, slider_S1, slider_n_points, slider_freq, anim_delay=100):

        self.max_epoch = 101
        self.T = 2
        self.pp0 = np.linspace(-1, 1, 201)
        self.tt0 = np.sin(2 * np.pi * self.pp0 / self.T)

        self.p = np.linspace(-1, 1, 21)

        # self.make_plot(1, (100, 90, 300, 300))
        # self.make_plot(2, (100, 380, 300, 300))
        

        self.train_error, self.error_train = [], None
        self.test_error, self.error_test = [], None
        self.gamma_list = []
        self.ani_1, self.ani_2, self.ani_3 = None, None, None
        self.W1, self.b1, self.W2, self.b2 = None, None, None, None
        self.random_state = 29
        np.random.seed(self.random_state)
        self.tt, self.t = None, None

        # self.axes_1 = self.figure.add_subplot(1, 1, 1)
        # self.axes_1.set_title("Function", fontdict={'fontsize': 10})
        # self.axes_1.set_xlim(-1, 1)
        # self.axes_1.set_ylim(-1.5, 1.5)
        # self.axes_1_blue_line, = self.axes_1.plot([], [], color="blue")
        # self.net_approx, = self.axes_1.plot([], linestyle="--", color="red")
        # self.train_points, = self.axes_1.plot([], marker='*', label="Train", linestyle="")
        # # self.test_points, = self.axes_1.plot([], marker='.', label="Test", linestyle="")
        # self.axes_1.legend()
        # self.canvas.draw()
        # self.function_plot = go.Scatter(x=self.pp0, y=self.tt0, mode='lines', name='Function')

        self.nsd = slider_nsd
        self.slider_nsd = slider_nsd

        self.animation_speed = 100

        self.S1 = slider_S1
        self.slider_S1 = slider_S1

        self.n_points = slider_n_points
        self.slider_n_points = slider_n_points

        self.freq = slider_freq
        self.slider_freq = slider_freq

        self.blue_line,self.train_points,self.test_points = self.plot_train_test_data()


        # self.blue_line = go.Scatter(x=[], y=[], mode='lines', name='Function', line=dict(color='blue'))
        self.net_approx = go.Scatter(x=[0], y=[0], mode='lines', name='Approximation', line=dict(color='red'))
        # self.train_points = go.Scatter(x=[], y=[], mode='markers', name='Train', marker=dict(color='blue', size=10))
        # self.test_points = go.Scatter(x=[], y=[], mode='markers', name='Test', marker=dict(color='black', size=10))

        self.figure1 = go.Figure(
            data=[self.blue_line,
                  self.net_approx, 
                  self.train_points,
                #   self.test_points
                  ],
            layout=go.Layout(
                title="Function Approximation",
                xaxis=dict(range=[-1, 1]),
                yaxis=dict(range=[-1.5, 1.5]),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Train",
                                  method="animate",
                                  args=[None, {"frame": {"duration": anim_delay, "redraw": False},
                                               "fromcurrent": False, "transition": {"duration": 900, "easing": "linear"}}])
                    ]
                )]
            ),
            frames=[],
        )

        # self.axes_2 = self.figure2.add_subplot(1, 1, 1)
        # self.axes_2.set_title("Performance Indexes", fontdict={'fontsize': 10})
        # self.train_e, = self.axes_2.plot([], [], linestyle='-', color="blue", label="train error")
        # self.test_e, = self.axes_2.plot([], [], linestyle='-', color="black", label="test error")
        # self.gamma, = self.axes_2.plot([], [], linestyle='-', color="red", label="gamma")
        # self.axes_2.legend()
        # self.axes_2.plot(1, 1000, marker="*")
        # self.axes_2.plot(100, 1000, marker="*")
        # self.axes_2.plot(1, 0.1, marker="*")
        # self.axes_2.plot(100, 0.1, marker="*")
        # self.axes_2.set_xscale("log")
        # self.axes_2.set_yscale("log")
        colors = ['#ff0000', 'green', 'blue', 'orange']

        self.four_star = go.Scatter(x=[1, 100, 100, 1, 1], y=[0.1, 0.1, 1000, 1000, 0.1], mode='markers', showlegend=False,
                                    marker=dict(color=colors, symbol='star', size=10))

        self.figure2 = go.Figure(
            data=[go.Scatter(x=[0], y=[0], mode='lines', name='Train Error', line=dict(color='blue')),
                  go.Scatter(x=[0], y=[0], mode='lines', name='Test Error', line=dict(color='black')),
                  go.Scatter(x=[0], y=[0], mode='lines', name='Gamma', line=dict(color='red')),
                  self.four_star],
            layout=go.Layout(
                title="Performance Indexes",
                xaxis=dict(type="log"),
                yaxis=dict(type="log"),

                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Train",
                                  method="animate",
                                #   mode="immediate",
                                  args=[None, {"frame": {"duration": anim_delay, "redraw": False},
                                               "fromcurrent": True, "transition": {"duration": 900, "easing": "linear"}}]),
                    ],
                )],
            ),
            frames=[],
        )



        

        # self.make_button("run_button", "Train", (self.x_chapter_button, 610, self.w_chapter_button, self.h_chapter_button), self.on_run)
        self.init_params()
        self.full_batch = False

        self.pp = np.linspace(-0.95, 0.95, self.n_points)
    
    def animate(self):
        self.animate_init_1()
        frame_1 = []
        frame_2 = []
        for idx in range(self.max_epoch):
            frame_1.append(go.Frame(data=self.on_animate_1(idx)))
            frame_2.append(go.Frame(data=[self.blue_line,
                                          self.on_animate_2(idx),
                                          self.train_points,
                                        #   self.test_points,
                                          ]))
            

        self.figure1.frames = frame_2
        self.figure2.frames = frame_1
        return self.figure1, self.figure2

    def animate_init_1(self):
        self.init_params()
        self.error_goal_reached = False
        self.a1 = self.tansig(np.dot(self.W1, self.pp.reshape(1, -1)) + self.b1)
        self.a2 = self.purelin(np.dot(self.W2, self.a1) + self.b2)
        self.e = self.tt.reshape(1, -1) - self.a2
        self.error_prev = np.dot(self.e, self.e.T).item()
        self.gamk = self.S1 * 3 + 1
        if self.error_prev == 0:
            self.beta = 1
        else:
            self.beta = (self.e.shape[1] - self.gamk) / (2 * self.error_prev)
        if self.beta <= 0:
            self.beta = 1
        self.reg = 0
        for param in [self.W1, self.b1, self.W2, self.b2]:
            self.reg += np.dot(param.reshape(1, -1), param.reshape(-1, 1)).item()
        self.alpha = self.gamk / (2 * self.reg)
        self.f1 = self.beta * self.error_prev + self.alpha * self.reg
        self.mu = 10
        self.RS = self.S1 * 1
        self.RS1 = self.RS + 1
        self.RSS = self.RS + self.S1
        self.RSS1 = self.RSS + 1
        self.RSS2 = self.RSS + self.S1 * 1
        self.RSS3 = self.RSS2 + 1
        self.RSS4 = self.RSS2 + 1
        self.ii = np.eye(self.RSS4)
        # self.train_e.set_data([], [])
        # self.test_e.set_data([], [])
        # self.gamma.set_data([], [])
        # self.net_approx.set_data([], [])
        # return self.train_e, self.test_e, self.gamma

    def animate_init_2(self):
        # self.net_approx.set_data([], [])
        return 

    def on_animate_1(self, idx):
        
        self.error_train, self.error_test, gamma = self.train_v2()
        self.gamma_list.append(gamma)
        self.train_error.append(self.error_train)
        # self.train_e.set_data(list(range(len(self.train_error))), self.train_error)
        train_e = go.Scatter(x=list(range(len(self.train_error))), y=self.train_error, mode='lines', name='Train Error', line=dict(color='blue'))
        self.test_error.append(self.error_test)
        # self.test_e.set_data(list(range(len(self.test_error))), self.test_error)
        test_e = go.Scatter(x=list(range(len(self.test_error))), y=self.test_error, mode='lines', name='Test Error', line=dict(color='black'))
        # self.gamma.set_data(list(range(len(self.gamma_list))), self.gamma_list)
        gamma = go.Scatter(x=list(range(len(self.gamma_list))), y=self.gamma_list, mode='lines', name='Gamma', line=dict(color='red'))
        return [train_e, test_e, gamma, self.four_star,]

    def on_animate_2(self, idx):
        nn_output = []
        for sample, target in zip(self.pp0, self.tt0):
            a, n2, n1, a1, a0 = self.forward(sample)
            nn_output.extend(a[0])
        # self.net_approx.set_data(self.pp0, nn_output)
        # print(nn_output)
        return go.Scatter(x=self.pp0, y=nn_output, mode='lines', name='Approximation', line=dict(color='red'))



    def on_run(self):
        self.init_params()

        self.train_error, self.test_error, self.gamma_list = [], [], []
  

    def run_animation(self):
        self.ani_stop()
        self.ani_1 = FuncAnimation(self.figure2, self.on_animate_1, init_func=self.animate_init_1, frames=self.max_epoch,
                                   interval=self.animation_speed, repeat=False, blit=True)
        self.ani_2 = FuncAnimation(self.figure, self.on_animate_2, init_func=self.animate_init_2, frames=self.max_epoch,
                                   interval=self.animation_speed, repeat=False, blit=True)

 

    def plot_train_test_data(self):
        # self.axes_1_blue_line.set_data(self.pp0, np.sin(2 * np.pi * self.pp0 * self.freq / self.T))
        self.pp = np.linspace(-0.95, 0.95, self.n_points)
        self.tt = np.sin(2 * np.pi * self.pp * self.freq / self.T) + np.random.uniform(-2, 2, self.pp.shape) * 0.2 * self.nsd
        # self.train_points.set_data(self.pp, self.tt)
        self.t = np.sin(2 * np.pi * self.p * self.freq / self.T) + np.random.uniform(-2, 2, self.p.shape) * 0.2 * self.nsd
        # # self.test_points.set_data(self.p, self.t)
        return [go.Scatter(x=self.pp0, y=np.sin(2 * np.pi * self.pp0 * self.freq / self.T), mode='lines', name='Function'),
                go.Scatter(x=self.pp, y=self.tt, mode='markers', name='Train', marker=dict(color='blue', size=10)),
                go.Scatter(x=self.p, y=self.t, mode='markers', name='Test', marker=dict(color='black', size=10))]
    

    def init_params(self):
        np.random.seed(self.random_state)
        # self.W1 = np.random.uniform(-0.5, 0.5, (self.S1, 1))
        # self.b1 = np.random.uniform(-0.5, 0.5, (self.S1, 1))
        pr = np.array([np.min(self.p), np.max(self.p)])
        r = 1
        magw = 0.7 * self.S1 ** (1 / r)
        w = magw * self.nnnormr(2 * np.random.uniform(-0.5, 0.5, (self.S1, r)) - 1)
        if self.S1 == 1:
            b = 0
        else:
            # b = magw*linspace(-1,1,s)'.*sign(w(:,1))
            b = magw * np.linspace(-1, 1, self.S1).T * np.sign(w[:, 0])
        x = 2 / (pr[1] - pr[0])
        y = 1 - pr[1] * x
        xp = x.T
        self.b1 = np.dot(w, y) + b.reshape(-1, 1)
        # w = w.*xp(ones(1,s),:)
        self.W1 = w * xp

        self.W2 = np.random.uniform(-0.5, 0.5, (1, self.S1))
        self.b2 = np.random.uniform(-0.5, 0.5, (1, 1))

    @staticmethod
    def nnnormr(m):
        _, mc = m.shape
        if mc == 1:
            return m / np.abs(m)
        else:
            # return sqrt(ones./(sum((m.*m)')))'*ones(1,mc).*m
            # return np.sqrt(np.ones())
            print("!")

    def forward(self, sample):
        a0 = sample.reshape(-1, 1)
        # Hidden Layer's Net Input
        n1 = np.dot(self.W1, a0) + self.b1
        #  Hidden Layer's Transformation
        a1 = self.tansig(n1)
        # Output Layer's Net Input
        n2 = np.dot(self.W2, a1) + self.b2
        # Output Layer's Transformation
        return self.purelin(n2), n2, n1, a1, a0

    def train(self):
        alpha = 0.03

        error_train, dw1, db1, dw2, db2 = [], 0, 0, 0, 0
        for sample, target in zip(self.pp, self.tt):
            a, n2, n1, a1, a0 = self.forward(sample)
            e = target - a
            error_train.append(e)
            # error = np.append(error, e)
            # Output Layer
            F2_der = np.diag(self.purelin_der(n2).reshape(-1))
            s = -2 * np.dot(F2_der, e)  # (s2 = s)
            # Hidden Layer
            F1_der = np.diag(self.logsigmoid_der(n1).reshape(-1))
            s1 = np.dot(F1_der, np.dot(self.W2.T, s))

            if self.full_batch:
                dw1 += np.dot(s1, a0.T)
                db1 += s1
                dw2 += np.dot(s, a1.T)
                db2 += s
            else:
                # Updates the weights and biases
                # Hidden Layer
                self.W1 += -alpha * np.dot(s1, a0.T)
                self.b1 += -alpha * s1
                # Output Layer
                self.W2 += -alpha * np.dot(s, a1.T)
                self.b2 += -alpha * s

        if self.full_batch:
            # Updates the weights and biases
            # Hidden Layer
            self.W1 += -alpha * dw1
            self.b1 += -alpha * db1
            # Output Layer
            self.W2 += -alpha * dw2
            self.b2 += -alpha * db2

        error_test = []
        for sample, target in zip(self.p, self.t):
            a, n2, n1, a1, a0 = self.forward(sample)
            e = target - a
            error_test.append(e)

        return np.sum(np.abs(error_train)), np.sum(np.abs(error_test))

    def train_v2(self):

        self.a1 = np.kron(self.a1, np.ones((1, 1)))
        d2 = self.lin_delta(self.a2)
        d1 = self.tan_delta(self.a1, d2, self.W2)
        jac1 = self.marq(np.kron(self.pp.reshape(1, -1), np.ones((1, 1))), d1)
        jac2 = self.marq(self.a1, d2)
        jac = np.hstack((jac1, d1.T))
        jac = np.hstack((jac, jac2))
        jac = np.hstack((jac, d2.T))
        je = np.dot(jac.T, self.e.T)

        grad = np.sqrt(np.dot(je.T, je)).item()
        if grad < 1e-8:
            error_test = []
            for sample, target in zip(self.p, self.t):
                a, n2, n1, a1, a0 = self.forward(sample)
                e = target - a
                error_test.append(e)
            return self.error_prev, np.sum(np.abs(error_test)), self.gamk

        jj = np.dot(jac.T, jac)
        w = np.copy(self.W1.reshape(-1, 1))
        for param in [self.b1, self.W2, self.b2]:
            w = np.vstack((w, param.reshape(-1, 1)))

        while self.mu < 1e10:

            dw = -np.dot(np.linalg.inv(self.beta * jj + (self.mu + self.alpha) * self.ii),
                         self.beta * je + self.alpha * w)
            dW1 = dw[:self.RS]
            db1 = dw[self.RS:self.RSS]
            dW2 = dw[self.RSS:self.RSS2].reshape(1, -1)
            db2 = dw[self.RSS2].reshape(1, 1)

            self.a1 = self.tansig(np.dot((self.W1 + dW1), self.pp.reshape(1, -1)) + self.b1 + db1)
            self.a2 = self.purelin(np.dot((self.W2 + dW2), self.a1) + self.b2 + db2)
            self.e = self.tt.reshape(1, -1) - self.a2
            error = np.dot(self.e, self.e.T).item()
            reg = 0
            for param in [self.W1 + dW1, self.b1 + db1, self.W2 + dW2, self.b2 + db2]:
                reg += np.dot(param.reshape(1, -1), param.reshape(-1, 1)).item()
            f2 = self.beta * error + self.alpha * reg

            if f2 < self.f1:
                self.W1 += dW1
                self.b1 += db1
                self.W2 += dW2
                self.b2 += db2
                self.error_prev = error
                self.reg = reg
                w = np.copy(self.W1.reshape(-1, 1))
                for param in [self.b1, self.W2, self.b2]:
                    w = np.vstack((w, param.reshape(-1, 1)))
                self.mu /= 2
                if self.mu < 1e-20:
                    self.mu = 1e-20
                break
            self.mu *= 2

        self.gamk = self.S1 * 3 + 1 - self.alpha * np.trace(np.linalg.inv(self.beta * jj + self.ii * self.alpha))
        if self.reg == 0:
            self.aplha = 1
        else:
            self.alpha = self.gamk / (2 * self.reg)
        if self.error_prev == 0:
            self.beta = 1
        else:
            self.beta = (self.e.shape[1] - self.gamk) / (2 * self.error_prev)
        self.f1 = self.beta * self.error_prev + self.alpha * self.reg

        if self.error_prev <= 0:
            if self.error_goal_reached:
                print("Error goal reached!")
                self.error_goal_reached = None
            error_test = []
            for sample, target in zip(self.p, self.t):
                a, n2, n1, a1, a0 = self.forward(sample)
                e = target - a
                error_test.append(e)
            return self.error_prev, np.sum(np.abs(error_test)), self.gamk

        error_test = []
        for sample, target in zip(self.p, self.t):
            a, n2, n1, a1, a0 = self.forward(sample)
            e = target - a
            error_test.append(e)
        return self.error_prev, np.sum(np.abs(error_test)), self.gamk
    
    @staticmethod
    def logsigmoid(n):
        return 1 / (1 + np.exp(-n))

    @staticmethod
    def logsigmoid_stable(n):
        n = np.clip(n, -100, 100)
        return 1 / (1 + np.exp(-n))

    @staticmethod
    def logsigmoid_der(n):
        return (1 - 1 / (1 + np.exp(-n))) * 1 / (1 + np.exp(-n))

    @staticmethod
    def purelin(n):
        return n

    @staticmethod
    def purelin_der(n):
        return np.array([1]).reshape(n.shape)

    @staticmethod
    def lin_delta(a, d=None, w=None):
        na, ma = a.shape
        if d is None and w is None:
            return -np.kron(np.ones((1, ma)), np.eye(na))
        else:
            return np.dot(w.T, d)

    @staticmethod
    def log_delta(a, d=None, w=None):
        s1, _ = a.shape
        if d is None and w is None:
            return -np.kron((1 - a) * a, np.ones((1, s1))) * np.kron(np.ones((1, s1)), np.eye(s1))
        else:
            return (1 - a) * a * np.dot(w.T, d)

    @staticmethod
    def tan_delta(a, d=None, w=None):
        s1, _ = a.shape
        if d is None and w is None:
            return -np.kron(1 - a * a, np.ones((1, s1))) * np.kron(np.ones((1, s1)), np.eye(s1))
        else:
            return (1 - a * a) * np.dot(w.T, d)

    @staticmethod
    def marq(p, d):
        s, _ = d.shape
        r, _ = p.shape
        return np.kron(p.T, np.ones((1, s))) * np.kron(np.ones((1, r)), d.T)

    @staticmethod
    def compet(n, axis=None):
        if axis is not None:
            max_idx = np.argmax(n, axis=axis)
            out = np.zeros(n.shape)
            for i in range(out.shape[1]):
                out[max_idx[i], i] = 1
            return out
        else:
            max_idx = np.argmax(n)
            out = np.zeros(n.shape)
            out[max_idx] = 1
            return out

    @staticmethod
    def poslin(n):
        return n * (n > 0)

    @staticmethod
    def hardlim(x):
        if x < 0:
            return 0
        else:
            return 1

    @staticmethod
    def hardlims(x):
        if x < 0:
            return -1
        else:
            return 1

    @staticmethod
    def satlin(x):
        if x < 0:
            return 0
        elif x < 1:
            return x
        else:
            return 1

    @staticmethod
    def satlins(x):
        if x < -1:
            return 0
        elif x < 1:
            return x
        else:
            return 1

    @staticmethod
    def logsig(x):
        return 1 / (1 + math.e ** (-x))

    @staticmethod
    def tansig(x):
        return 2 / (1 + math.e ** (-2 * x)) - 1

    def nndtansig(self, x):
        self.a = self.tansig(x)


if __name__=="__main__":

    st.set_page_config(page_title='Neural Network DESIGN', page_icon='🧠', layout='centered', initial_sidebar_state='auto')



    def load_svg(svg_file):
        with open(svg_file, "r", encoding="utf-8") as f:
            svg = f.read()
        svg_base64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
        # Adjust 'max-width' to increase the size of the image, for example, to 60% of its container
        # You can also adjust 'height' if necessary, but 'auto' should maintain the aspect ratio
        svg_html = f'''
        <div style="text-align: left; width: 100%;">
            <img src="data:image/svg+xml;base64,{svg_base64}" alt="SVG Image" style="max-width: 80%; height: 100px; margin: 10px;">
        </div>
        '''
        return svg_html


    def get_image_path(filename):
        # Use a raw string for the path
        return os.path.join(image_path, filename)


    hide_pages(pages_created)

    image_path = 'media/Logo/book_logos'
    with open('media/CSS/home_page.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    header_cols = st.columns([4, 2])
    with header_cols[1]:
        st.text('')
        st.subheader('Bayesian Regularization')
        # st.subheader('')
    
    with header_cols[0]:
        st.subheader('*Neural Network*')
        st.subheader('DESIGN')
    
    st.markdown('---')

    with st.sidebar:
        st.markdown(load_svg(get_image_path("13.svg")), unsafe_allow_html=True)
        st.markdown("Click the [Train] button to train the logsig-linear network on the data points.")
        st.markdown("Use the slide bars to choose the number of neurons and the difficulty of the data points.")
        slider_nsd = st.slider("Noise standard deviation:", 0.0, 3.0, 1.0)
        slider_S1 = st.slider("#Hidden Neurons:", 2, 40, 18)
        slider_n_points = st.slider("#Data Points:", 10, 40, 24)
        slider_freq = st.slider("Frequency:", 0.5, 4.0, 1.67)
        st.subheader('*Chapter13*')
        st.markdown('---')

        # anim_delay = st.slider("Animation Delay:", 0, 50, 10, step=1) * 10

    app = BayesianRegularization(slider_nsd, slider_S1, slider_n_points, slider_freq)

    fig1, fig2 = app.animate()
    fig1.update_layout(
        legend=dict(x=0.5, y=-0.2, xanchor='center', yanchor='top'), # Adjust y to move legend inside subplot
        legend_orientation='h',
        legend_font_size=15,
        # font_family='Droid Sans',
        font=dict(family='Droid Sans', size=15, color='black'),
        xaxis_title="Input",
        xaxis_title_font_color='black',
        yaxis_title="Target",
        yaxis_title_font_color='black',
    )

    fig2.update_layout(
        legend=dict(x=0.5, y=-0.2, xanchor='center', yanchor='top'), # Adjust y to move legend inside subplot
        legend_orientation='h',
        legend_font_size=15,
        # font_family='Droid Sans',
        font=dict(family='Droid Sans', size=15, color='black'),
        xaxis_title="Epoch",
        xaxis_title_font_color='black',
        yaxis_title="Error",
        yaxis_title_font_color='black',
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)
    