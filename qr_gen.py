import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox
import tkinter.filedialog
import time
import qrcode
from qrcode.image.svg import SvgImage


class QR_Gen_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        # title
        self.title("LB's QR Code Generator")

        # constants
        CCB_WIDTH = 8
        NAMED_COLORS = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
        FC_DEFAULT_INDEX = NAMED_COLORS.index("black")
        BC_DEFAULT_INDEX = NAMED_COLORS.index("white")
        VERSIONS = [n for n in range(1, 41)]
        VERSIONS.insert(0, "auto")
        DEFAULT_VERSION_INDEX = VERSIONS.index("auto")
        self.FORMATS = {"png":"png", "svg":"svg"}
        self.FILE_TYPES=(("png file", ".png"), ("svg file", ".svg"))

        # main frame
        main_frame = ttk.Frame(self, padding=5)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # responsiveness of main frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # text
        text_frame = ttk.Labelframe(main_frame, text="Text to encode:")
        text_frame.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)
        self.text = text = tk.Text(text_frame, height=6)
        text.pack(fill=tk.BOTH, expand=True)

        # parameters
        params_frame = ttk.Labelframe(main_frame, text="Parameters:")
        params_frame.grid(row=1, column=0, sticky=tk.NSEW, pady=5, padx=5)

        # responsiveness of parameters frame
        params_frame.grid_rowconfigure(0, weight=1)
        params_frame.grid_columnconfigure(0, weight=1)
        params_frame.grid_columnconfigure(1, weight=1)
        params_frame.grid_columnconfigure(2, weight=1)

        ## cbb version
        frm_version = ttk.Frame(params_frame)
        lbl_version = ttk.Label(frm_version, text="Version:")
        self.cbb_version = cbb_version = ttk.Combobox(frm_version, width=CCB_WIDTH)
        cbb_version['values'] = VERSIONS
        cbb_version['state'] = 'readonly'
        cbb_version.current(DEFAULT_VERSION_INDEX)
        lbl_version.grid(row=0, column=0, padx=2)
        cbb_version.grid(row=0, column=1, padx=2)
        frm_version.grid(row=0, column=0, padx=5, pady=5)

        ## cbb front color
        frm_fc = ttk.Frame(params_frame)
        lbl_fc = ttk.Label(frm_fc, text="Front Color:")
        self.cbb_fc = cbb_fc = ttk.Combobox(frm_fc, width=CCB_WIDTH)
        cbb_fc['values'] = NAMED_COLORS
        cbb_fc['state'] = 'readonly'
        cbb_fc.current(FC_DEFAULT_INDEX)
        lbl_fc.grid(row=0, column=0, padx=2)
        cbb_fc.grid(row=0, column=1, padx=2)
        frm_fc.grid(row=0, column=1, padx=5, pady=5)

        ## cbb back color
        frm_bc = ttk.Frame(params_frame)
        lbl_bc = ttk.Label(frm_bc, text="Back Color:")
        self.cbb_bc = cbb_bc = ttk.Combobox(frm_bc, width=CCB_WIDTH)
        cbb_bc['values'] = NAMED_COLORS
        cbb_bc['state'] = 'readonly'
        cbb_bc.current(BC_DEFAULT_INDEX)
        lbl_bc.grid(row=0, column=0, padx=2)
        cbb_bc.grid(row=0, column=1, padx=2)
        frm_bc.grid(row=0, column=2, padx=5, pady=5)

        ## rd output format
        frm_output_format = ttk.Frame(params_frame)
        lbl_of = ttk.Label(frm_output_format, text="Output Format:")
        self.str_var_of = str_var_of = tk.StringVar(None)
        str_var_of.set(self.FORMATS["png"])
        rd_png = ttk.Radiobutton(frm_output_format, text=self.FORMATS["png"], value=self.FORMATS["png"], variable=str_var_of)
        rd_svg = ttk.Radiobutton(frm_output_format, text=self.FORMATS["svg"], value=self.FORMATS["svg"], variable=str_var_of)
        lbl_of.grid(row=0, column=0, padx=2)
        rd_png.grid(row=0, column=1, padx=2)
        rd_svg.grid(row=0, column=2, padx=2)
        frm_output_format.grid(row=1, column=2, padx=5, pady=5)

        # gen button
        gen_btn_frame = ttk.Frame(main_frame)
        gen_btn_frame.grid(row=1, column=1, padx=5, pady=5)
        btn_gen = ttk.Button(gen_btn_frame, text="Generate", command=self._generate_qr)
        btn_gen.pack(padx=5, pady=5)

    def _generate_qr(self):
        VERSION = self.cbb_version.get()
        FILL_COLOR = self.cbb_fc.get()
        BACK_COLOR = self.cbb_bc.get()
        FORMAT = self.str_var_of.get()
        STR = self.text.get("1.0", tk.END)

        if STR.strip() == "":
            tk.messagebox.showerror("Error", "Can't generate QR code on empty content.")
            return

        qr_generator = qrcode.QRCode(version=None if VERSION=="auto" else VERSION)
        qr_generator.add_data(STR)
        qr_generator.make(fit=True)

        if FORMAT == self.FORMATS["svg"]:
            img = qr_generator.make_image(fill_color=FILL_COLOR, back_color=BACK_COLOR, image_factory=SvgImage)
            ts = int(time.time())
            initial_filename = f"qr_{ts}.svg"
            filename = tk.filedialog.asksaveasfilename(title="filename", initialfile=initial_filename, filetypes=self.FILE_TYPES, defaultextension=".svg")
        else:
            img = qr_generator.make_image(fill_color=FILL_COLOR, back_color=BACK_COLOR)
            ts = int(time.time())
            initial_filename = f"qr_{ts}.png"
            filename = tk.filedialog.asksaveasfilename(title="filename", initialfile=initial_filename, filetypes=self.FILE_TYPES, defaultextension=".png")

        if not filename:
            return
        
        try:
            img.save(filename)
            tk.messagebox.showinfo("Saved", "QR Code saved!")
        except:
            tkinter.messagebox.showerror("Error", "Error saving file!")
    
    def run(self):
        self.mainloop()


def launcher():
    app = QR_Gen_Window()
    app.run()


if __name__ == "__main__":
    launcher()