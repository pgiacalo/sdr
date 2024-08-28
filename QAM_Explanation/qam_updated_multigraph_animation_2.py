"""
Program Name: QAM Simulation

Description: A program that simulates RF quadrature amplitude modulation (QAM)

Author: Philip Giacalone

Date Created: 2024-08-28
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.animation import FuncAnimation
from scipy import special
import logging

logging.basicConfig(level=logging.INFO)

class QAMSimulation:

    def __init__(self):
        self.frequency = 1
        self.sampling_rate = 1000
        self.duration = 1
        self.t = np.linspace(0, self.duration, int(self.duration * self.sampling_rate), endpoint=False)
        self.t_degrees = 360 * self.t / self.duration
        
        self.M = 16
        self.I_values = self.Q_values = np.array([-3, -1, 1, 3])
        self.binary_values = [f"{i:0{int(np.log2(self.M))}b}" for i in range(self.M)]
        self.qam_signal, _ = self.qam_modulate(self.I_values, self.Q_values, self.binary_values)
        
        self.A = 1
        self.B = 1
        
        self.max_trail_length = 100
        self.trail_points = []
        self.trail = None
        
        self.anim = None
        
        self.streaming = False
        self.bit_sequence = self.generate_bit_sequence()
        self.current_bit_index = 0
        self.symbol_duration = 40  # 40 frames * 50ms = 2 seconds
        self.highlight_duration = 10  # 10 frames * 50ms = 0.5 seconds for red highlight
        self.frame_counter = 0
        
        self.setup_plot()
        self.setup_controls()
        self.update_plot(None)

    def qam_modulate(self, I_values, Q_values, binary_values):
        X, Y = np.meshgrid(I_values, Q_values)
        X = X.flatten()
        Y = Y.flatten()
        constellation = X + 1j * Y
        return constellation, dict(zip(binary_values, constellation))

    def calculate_evm(self, signal, ideal_signal):
        error = signal - ideal_signal
        rms_error = np.sqrt(np.mean(np.abs(error) ** 2))
        rms_signal = np.sqrt(np.mean(np.abs(ideal_signal) ** 2))
        return (rms_error / rms_signal) * 100 if rms_signal != 0 else 0

    def calculate_ber(self, snr_db):
        snr = 10**(snr_db/10)
        ber = 4 * (1 - 1/np.sqrt(self.M)) * special.erfc(np.sqrt(3*snr/(2*(self.M-1)))) / np.log2(self.M)
        return ber

    def setup_plot(self):
        self.fig, (self.ax_const, self.ax_waves) = plt.subplots(1, 2, figsize=(15, 7))
        plt.subplots_adjust(left=0.1, right=0.9, bottom=0.25, top=0.9)

        self.fig.patch.set_facecolor('white')
        self.ax_const.set_facecolor('white')
        self.ax_waves.set_facecolor('white')

        self.setup_constellation_diagram()
        self.setup_waveform_plot()


    def generate_bit_sequence(self):
        all_symbols = list(range(16))
        np.random.shuffle(all_symbols)
        bit_sequence = []
        for symbol in all_symbols:
            bit_sequence.extend([int(b) for b in f"{symbol:04b}"])
        return np.array(bit_sequence)

    def format_bit_string(self, bit_string, highlight_start=None):
        formatted = ' '.join(bit_string[i:i+4] for i in range(0, len(bit_string), 4))
        if highlight_start is not None:
            group_start = (highlight_start // 4) * 5  # Start of the group containing the highlight
            offset = highlight_start % 4
            
            # Add two spaces before underlining to shift it two characters to the right
            underline_start = group_start + offset + 1
            
            formatted = (formatted[:underline_start] +
                         '\u0332' + '\u0332'.join(formatted[underline_start:underline_start+4]) +
                         formatted[underline_start+4:])
        
        return formatted

    def setup_constellation_diagram(self):
        self.scatter = self.ax_const.scatter(np.real(self.qam_signal), np.imag(self.qam_signal), color='blue', zorder=5, picker=True)
        self.highlighted_point = self.ax_const.scatter([], [], marker='o', color='red', s=100, zorder=10)
        for i, (x, y) in enumerate(zip(np.real(self.qam_signal), np.imag(self.qam_signal))):
            self.ax_const.text(x, y + 0.2, self.binary_values[i], ha='center', va='center')

        self.ax_const.set_title(f'{self.M}-QAM Constellation Diagram')
        self.ax_const.set_xlim(-5, 5)
        self.ax_const.set_ylim(-5, 5)
        self.ax_const.set_xticks(np.arange(-5, 6, 1))
        self.ax_const.set_yticks(np.arange(-5, 6, 1))
        self.ax_const.axhline(0, color='lightgray', linestyle='-')
        self.ax_const.axvline(0, color='lightgray', linestyle='-')
        self.ax_const.grid(True)
        self.ax_const.set_xlabel('In-Phase, I (Cosine)')
        self.ax_const.set_ylabel('Quadrature, Q (Sine)')

        circle_radii = [np.sqrt(2), np.sqrt(10), np.sqrt(18)]
        for radius in circle_radii:
            circle = plt.Circle((0, 0), radius, fill=False, linestyle='--', color='lightgray')
            self.ax_const.add_artist(circle)
            self.ax_const.text(0, radius + 0.3, f'r = {radius:.2f}', color='black', ha='center', va='bottom')

        for point in self.qam_signal:
            angle = np.angle(point)
            self.ax_const.plot([0, 5*np.cos(angle)], [0, 5*np.sin(angle)], linestyle='--', color='lightgray', zorder=1)

        self.trail = self.ax_const.scatter([], [], color='red', alpha=0.1, s=20, zorder=4)
        
        self.bit_text = self.ax_const.text(0.05, 1.05, "", transform=self.ax_const.transAxes, fontsize=12, fontweight='bold')


    def setup_waveform_plot(self):
        self.line1, = self.ax_waves.plot(self.t_degrees, np.zeros_like(self.t), 'r', label='Sine (Q)')
        self.line2, = self.ax_waves.plot(self.t_degrees, np.zeros_like(self.t), 'g', label='Cosine (I)')
        self.line3, = self.ax_waves.plot(self.t_degrees, np.zeros_like(self.t), 'b', label='Combination')

        self.ax_waves.set_title('Waveforms')
        self.ax_waves.set_xlim(0, 360)
        self.ax_waves.set_ylim(-5, 5)
        self.ax_waves.set_xlabel('Angle')
        self.ax_waves.set_xticks(np.arange(0, 360 + 90, 90))
        self.ax_waves.set_xticklabels([f'{int(tick)}°' for tick in np.arange(0, 360 + 90, 90)])
        self.ax_waves.axvline(180, color='grey', linestyle='--')
        self.ax_waves.grid(which='both', linestyle='--')
        self.ax_waves.set_yticks(np.arange(-5, 6, 1))
        self.ax_waves.legend()

        # Only keep Amplitude and Phase text, moved to upper left
        self.amp_phase_text = self.ax_waves.text(0.02, 0.98, "", ha='left', va='top', transform=self.ax_waves.transAxes)

        # Comment out EVM and BER text
        # self.evm_text = self.ax_waves.text(0.02, 0.85, "", ha='left', va='top', transform=self.ax_waves.transAxes)
        # self.ber_text = self.ax_waves.text(0.02, 0.75, "", ha='left', va='top', transform=self.ax_waves.transAxes)


    def setup_controls(self):
        axAmp1 = plt.axes([0.1, 0.15, 0.3, 0.03])
        self.sAmp1 = Slider(axAmp1, 'Sine Amplitude (Q)', -3, 3, valinit=1, valstep=0.1, valfmt='%1.1f')

        axAmp2 = plt.axes([0.1, 0.1, 0.3, 0.03])
        self.sAmp2 = Slider(axAmp2, 'Cosine Amplitude (I)', -3, 3, valinit=1, valstep=0.1, valfmt='%1.1f')

        axNoise = plt.axes([0.55, 0.1, 0.35, 0.03])
        self.sNoise = Slider(axNoise, 'Noise Level', 0, 1, valinit=0.05, valstep=0.01, valfmt='%1.2f')

        rax = plt.axes([0.3, 0.02, 0.4, 0.04])
        self.radio = RadioButtons(rax, ('2-BPSK', '4-QPSK', '16-QAM'), active=2)

        tutorial_ax = plt.axes([0.72, 0.02, 0.1, 0.04])
        self.tutorial_button = Button(tutorial_ax, 'Tutorial')

        stream_ax = plt.axes([0.82, 0.02, 0.1, 0.04])
        self.stream_button = Button(stream_ax, 'Start Animation')

        self.sAmp1.on_changed(self.update_plot)
        self.sAmp2.on_changed(self.update_plot)
        self.fig.canvas.mpl_connect('pick_event', self.on_pick)
        self.fig.canvas.mpl_connect('motion_notify_event', self.hover)
        self.radio.on_clicked(self.change_modulation)
        self.tutorial_button.on_clicked(self.show_tutorial)
        self.stream_button.on_clicked(self.toggle_stream)


    def update_waveforms(self):
        sine_wave = self.A * np.sin(2 * np.pi * self.frequency * self.t)
        cosine_wave = self.B * np.cos(2 * np.pi * self.frequency * self.t)
        resultant_waveform = sine_wave + cosine_wave

        self.line1.set_ydata(sine_wave)
        self.line2.set_ydata(cosine_wave)
        self.line3.set_ydata(resultant_waveform)

        self.highlighted_point.set_offsets([[self.B, self.A]])

        evm = self.calculate_evm(resultant_waveform, resultant_waveform)
        # self.evm_text.set_text(f"EVM: {evm:.2f}%")

        amplitude = np.sqrt(self.A**2 + self.B**2)
        phase = np.arctan2(self.A, self.B) * 180 / np.pi
        self.amp_phase_text.set_text(f"Amplitude: {amplitude:.2f}\nPhase: {phase:.2f}°")

        snr_db = 20 * np.log10(amplitude / self.sNoise.val) if self.sNoise.val > 0 else float('inf')
        ber = self.calculate_ber(snr_db)
        # self.ber_text.set_text(f"BER: {ber:.2e}")

        self.fig.canvas.draw_idle()

    def update_plot(self, val):
        self.A = round(self.sAmp1.val, 1)
        self.B = round(self.sAmp2.val, 1)
        self.update_waveforms()
        self.highlighted_point.set_offsets([[self.B, self.A]])


    def on_pick(self, event):
        index = event.ind[0]
        I, Q = np.real(self.qam_signal)[index], np.imag(self.qam_signal)[index]
        self.sAmp2.set_val(I)
        self.sAmp1.set_val(Q)
        self.update_plot(None)

    def hover(self, event):
        if event.inaxes == self.ax_const:
            cont, _ = self.scatter.contains(event)
            if cont:
                self.ax_const.set_title(f'{self.M}-QAM Constellation Diagram (Hovering)', color='black')
            else:
                self.ax_const.set_title(f'{self.M}-QAM Constellation Diagram', color='black')
            self.fig.canvas.draw_idle()


    def get_symbol_for_bits(self, bits):
        bit_string = ''.join(map(str, bits))
        index = int(bit_string, 2)
        return self.qam_signal[index]



    def animate(self, frame):
        if self.streaming:
            if self.frame_counter == 0:
                bits = self.bit_sequence[self.current_bit_index:self.current_bit_index+4]
                full_bit_string = ''.join(map(str, self.bit_sequence))
                formatted_bits = self.format_bit_string(full_bit_string, self.current_bit_index)
                self.bit_text.set_text(f"Bits: {formatted_bits}")

                symbol = self.get_symbol_for_bits(bits)
                self.highlighted_point.set_offsets([[np.real(symbol), np.imag(symbol)]])

                self.sAmp2.set_val(np.real(symbol))
                self.sAmp1.set_val(np.imag(symbol))
                self.update_plot(None)

                self.current_bit_index = (self.current_bit_index + 4) % len(self.bit_sequence)

            self.frame_counter = (self.frame_counter + 1) % self.symbol_duration

        noise_amplitude = self.sNoise.val
        noise_i = np.random.normal(0, noise_amplitude)
        noise_q = np.random.normal(0, noise_amplitude)
        noisy_I = self.B + noise_i
        noisy_Q = self.A + noise_q
        
        self.trail_points.append((noisy_I, noisy_Q))
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points = self.trail_points[-self.max_trail_length:]
        
        if self.trail_points:
            x, y = zip(*self.trail_points)
            self.trail.set_offsets(np.c_[x, y])
        
        noisy_sine = self.A * np.sin(2 * np.pi * self.frequency * self.t) + noise_q
        noisy_cosine = self.B * np.cos(2 * np.pi * self.frequency * self.t) + noise_i
        noisy_resultant = noisy_sine + noisy_cosine
        
        self.line1.set_ydata(noisy_sine)
        self.line2.set_ydata(noisy_cosine)
        self.line3.set_ydata(noisy_resultant)
        
        amplitude = np.sqrt(noisy_I**2 + noisy_Q**2)
        phase = np.arctan2(noisy_Q, noisy_I) * 180 / np.pi
        self.amp_phase_text.set_text(f"Amplitude: {amplitude:.2f}\nPhase: {phase:.2f}°")
        
        self.fig.canvas.draw_idle()

        return [self.highlighted_point, self.trail, self.line1, self.line2, self.line3, 
                self.amp_phase_text, self.bit_text]

    def change_modulation(self, label):
        self.M = int(label.split('-')[0])
        
        if self.M == 2:  # BPSK
            self.I_values = np.array([-1, 1])
            self.Q_values = np.array([0])
        elif self.M == 4:  # QPSK
            self.I_values = self.Q_values = np.array([-1, 1])
            self.A = 0  # Set default sine amplitude to 0 for QPSK
            self.sAmp1.set_val(0)  # Update slider value
        else:  # 16-QAM
            self.I_values = self.Q_values = np.array([-3, -1, 1, 3])
        
        self.binary_values = [f"{i:0{int(np.log2(self.M))}b}" for i in range(self.M)]
        self.qam_signal, _ = self.qam_modulate(self.I_values, self.Q_values, self.binary_values)
        
        self.scatter.set_offsets(np.column_stack((np.real(self.qam_signal), np.imag(self.qam_signal))))
        
        for txt in self.ax_const.texts:
            txt.remove()
        for i, (x, y) in enumerate(zip(np.real(self.qam_signal), np.imag(self.qam_signal))):
            self.ax_const.text(x, y + 0.2, self.binary_values[i], ha='center', va='center')
        
        self.ax_const.set_title(f'{self.M}-QAM Constellation Diagram')
        self.update_plot(None)

    def show_tutorial(self, event):
        tutorial_text = """
        QAM Modulation Tutorial:
        
        1. Constellation Diagram:
           • Each point represents a unique symbol
           • X-axis: In-phase (I) component
           • Y-axis: Quadrature (Q) component
        
        2. Waveforms:
           • Red: Sine wave (Q component)
           • Green: Cosine wave (I component)
           • Blue: Combined QAM signal
        
        3. Sliders:
           • Adjust amplitudes of I and Q components
           • Control noise level
        
        4. Interaction:
           • Click on constellation points
           • Hover over constellation diagram
           • Change modulation order

                
        Experiment with different settings to see
        how they affect the signals and errors.
        """
        # 5. Metrics:
        #    • EVM (Error Vector Magnitude):
        #      - Measures difference between ideal and actual received symbol
        #      - Higher EVM indicates more distortion
        #    • BER (Bit Error Rate):
        #      - Ratio of incorrect bits to total bits
        #      - Lower BER indicates better quality

        plt.figure(figsize=(10, 8))
        plt.text(0.05, 0.95, tutorial_text, fontsize=12, va='top')
        plt.axis('off')
        plt.title("QAM Modulation Tutorial")
        plt.show()


    def run(self):
        logging.info("Starting QAM simulation")
        self.anim = FuncAnimation(self.fig, self.animate, frames=None, interval=50, blit=False, cache_frame_data=False)
        if self.anim.event_source is None:
            logging.warning("Animation event source is None. Creating a new one.")
            self.anim.event_source = self.anim._get_timer()
        self.anim.event_source.start()
        self.fig.canvas.mpl_connect('close_event', self.on_close)
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        plt.show()


    def toggle_stream(self, event):
        self.streaming = not self.streaming
        self.stream_button.label.set_text('Stop Animation' if self.streaming else 'Start Animation')
        if self.streaming:
            self.current_bit_index = 0
            self.frame_counter = 0
        else:
            # Clear the highlighted point safely
            self.highlighted_point.set_offsets(np.empty((0, 2)))
            self.bit_text.set_text("")
        self.fig.canvas.draw_idle()

    def on_click(self, event):
        if event.inaxes == self.ax_const and not self.streaming:
            cont, ind = self.scatter.contains(event)
            if cont:
                i, q = self.qam_signal[ind['ind'][0]].real, self.qam_signal[ind['ind'][0]].imag
                self.sAmp2.set_val(i)
                self.sAmp1.set_val(q)
                self.update_plot(None)
                # Update the red dot position
                self.highlighted_point.set_offsets([[i, q]])
                self.fig.canvas.draw_idle()


    def on_close(self, event):
        logging.info("Window close event triggered")
        if self.anim is not None:
            logging.info("Attempting to stop animation")
            try:
                if hasattr(self.anim, 'event_source') and self.anim.event_source is not None:
                    self.anim.event_source.stop()
                elif hasattr(self.anim, '_stop'):
                    self.anim._stop()
                else:
                    logging.warning("No method found to stop animation")
            except Exception as e:
                logging.error(f"Error stopping animation: {e}")
        
        logging.info("Clearing trail points")
        self.trail_points.clear()
        if self.trail is not None:
            self.trail.remove()
            self.trail = None
        
        logging.info("Closing all figures")
        plt.close('all')
        
        logging.info("Clearing animation reference")
        self.anim = None

if __name__ == "__main__":
    logging.info("Starting main program")
    qam_sim = QAMSimulation()
    qam_sim.run()
