from tkinter import Tk
import DailyReport
import TaxInvoiceManager
import DepositManager
import CostManager
import DrMenu


class Gui(Tk):
    def __init__(self):
        Tk.__init__(self)

        menubar = DrMenu.MenuBar(self)
        self.config(menu=menubar)

        self._frame = None
        self.switch_frame(DailyReport.DailyReport)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(expand=True, fill='both')

    def call_daily_report(self):
        self.switch_frame(DailyReport.DailyReport)

    def call_tax_invoice_manager(self):
        self.switch_frame(TaxInvoiceManager.TaxInvoiceManager)

    def call_deposit_manager(self):
        self.switch_frame(DepositManager.DepositManager)

    def call_cost_manager(self):
        self.switch_frame(CostManager.CostManager)

    def app_quit(self):
        # print('end')
        self.destroy()


class InitApp:
    def __init__(self):
        self.root = Gui()
        self.fullScreenState = True
        self.root.attributes("-fullscreen", self.fullScreenState)

        self.root.bind("<F11>", self.toggle_full_screen)
        self.root.bind("<Escape>", self.quit_full_screen)

        self.root.mainloop()

    def toggle_full_screen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)

    def quit_full_screen(self, event):
        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)


if __name__ == '__main__':
    app = InitApp()
