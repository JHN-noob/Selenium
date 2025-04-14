import tkinter.ttk as ttk
import webbrowser
import threading
from tkinter import *
from tkinter import messagebox
from flight_searcher import run_crawling



root = Tk()
root.title("Flight Searcher")

def link_open():
    webbrowser.open(f"https://flight.naver.com/flights/international/{flight_info.출발지}-{flight_info.도착지}-2025{flight_info.출발월일}/{flight_info.도착지}-{flight_info.출발지}-2025{flight_info.도착월일}?adult=1&isDirect={str(flight_info.직항).lower()}&fareType=Y")

class flight_info:
    def __init__(self):
        self.출발지 = ''
        self.도착지 = ''
        self.출발월일 = ''
        self.도착월일 = ''
        self.직항 = 0

def get_calandar():
    list_box.delete(0, END)
    loading_bar.start(10)
    search_btn.config(state="disabled")
    search_btn.update_idletasks()
    dep_kor = cmb_dep.get()
    flight_info.출발지 = opt_dep.get(dep_kor)
    arr_kor = cmb_arr.get()
    flight_info.도착지 = opt_arr.get(arr_kor)
    flight_info.출발월일 = cmb_dep_mon.get().zfill(2)+cmb_dep_day.get().zfill(2)
    flight_info.도착월일 = cmb_arr_mon.get().zfill(2)+cmb_arr_day.get().zfill(2)
    flight_info.직항 = direct_var.get()
    def run():
        결과 = run_crawling(flight_info.출발지, flight_info.도착지, flight_info.출발월일, flight_info.도착월일, str(flight_info.직항).lower())
        if 결과 is None:
            loading_bar.after(0, loading_bar.stop)
            search_btn.after(0, lambda: search_btn.config(state="normal"))
            messagebox.showinfo("검색 실패", "결과가 없거나 로딩에 실패했습니다.")
            return
        flight_company_text, n_times_text, n_cost_times_text, n_costs_text = 결과
        list_box.after(0, lambda: show_results(flight_company_text, n_times_text, n_cost_times_text, n_costs_text))
        nav_btn.after(0, lambda: nav_btn.config(state="normal"))
        search_btn.after(0, lambda: search_btn.config(state="normal"))
        loading_bar.after(0, loading_bar.stop)
    threading.Thread(target=run).start()

def show_results(flight_company_text, n_times_text, n_cost_times_text, n_costs_text):
    for i in range(len(flight_company_text)):
        항공사 = flight_company_text[i]
        if "," in 항공사:
            항공사 = 항공사.split(",")[0].strip() + " 외"
        출발도착시간 = n_times_text[i]
        소요시간 = n_cost_times_text[i]
        가격 = n_costs_text[i]

        result = f"{항공사:<10}  ||  출발시간: {출발도착시간[0]} → {출발도착시간[1]} / {소요시간[0]} | 도착시간: {출발도착시간[2]} → {출발도착시간[3]} / {소요시간[1]}  ||  {가격}원"
        list_box.insert(END, result)



# 일정 선택 라벨 프레임
choose_frame = LabelFrame(root, text="일정 선택")
choose_frame.pack(padx=5, pady=5, ipadx=5, ipady=5)
# 출발지 프레임 & 콤보박스
dep_frame = Frame(choose_frame)
dep_frame.pack(side="left", padx=10)
dep = Label(dep_frame, text="출발지", width=8)
dep.pack(padx=5, pady=5)
opt_dep = {"인천": "ICN", "제주": "CJU", "도쿄": "HND", "오사카": "KIX", "베이징": "PEK", "상하이": "PVG", "타이베이": "TSA", "하노이": "HAN", "방콕": "BKK", "런던": "LHR", "파리": "CDG", "베를린": "BER", "취리히": "ZRH", "부다페스트": "BUD", "밀라노": "LIN", "마드리드": "MAD", "시카오": "ORD", "로스앤젤레스": "LAX", "뉴욕": "JFK", "토론토": "YYZ", "시드니": "SYD"}
cmb_dep = ttk.Combobox(dep_frame, state="readonly", values=list(opt_dep.keys()), width=10)
cmb_dep.current(0)
cmb_dep.pack(padx=5, pady=5)
# 도착지 프레임 & 콤보박스
arr_frame = Frame(choose_frame)
arr_frame.pack(side="left", padx=10)
arr = Label(arr_frame, text="도착지", width=8)
arr.pack(padx=5, pady=5)
opt_arr = {"인천": "ICN", "제주": "CJU", "도쿄": "HND", "오사카": "KIX", "베이징": "PEK", "상하이": "PVG", "타이베이": "TSA", "하노이": "HAN", "방콕": "BKK", "런던": "LHR", "파리": "CDG", "베를린": "BER", "취리히": "ZRH", "부다페스트": "BUD", "밀라노": "LIN", "마드리드": "MAD", "시카오": "ORD", "로스앤젤레스": "LAX", "뉴욕": "JFK", "토론토": "YYZ", "시드니": "SYD"}
cmb_arr = ttk.Combobox(arr_frame, state="readonly", values=list(opt_arr.keys()), width=10)
cmb_arr.current(0)
cmb_arr.pack(padx=5, pady=5)
# 출발월 프레임 & 콤보박스
dep_mon_frame = Frame(choose_frame)
dep_mon_frame.pack(side="left", padx=10)
dep_mon = Label(dep_mon_frame, text="출발월", width=8)
dep_mon.pack(padx=5, pady=5)
opt_dep_mon = [i for i in range(1, 13)]
cmb_dep_mon = ttk.Combobox(dep_mon_frame, state="readonly", values=opt_dep_mon, width=3)
cmb_dep_mon.current(0)
cmb_dep_mon.pack(padx=5, pady=5)
# 출발일 프레임 & 콤보박스
dep_day_frame = Frame(choose_frame)
dep_day_frame.pack(side="left", padx=10)
dep_day = Label(dep_day_frame, text="출발일", width=8)
dep_day.pack(padx=5, pady=5)
opt_dep_day = [i for i in range(1, 32)]
cmb_dep_day = ttk.Combobox(dep_day_frame, state="readonly", values=opt_dep_day, width=3)
cmb_dep_day.current(0)
cmb_dep_day.pack(padx=5, pady=5)
# 도착월 프레임 & 콤보박스
arr_mon_frame = Frame(choose_frame)
arr_mon_frame.pack(side="left", padx=10)
arr_mon = Label(arr_mon_frame, text="도착월", width=8)
arr_mon.pack(padx=5, pady=5)
opt_arr_mon = [i for i in range(1, 13)]
cmb_arr_mon = ttk.Combobox(arr_mon_frame, state="readonly", values=opt_arr_mon, width=3)
cmb_arr_mon.current(0)
cmb_arr_mon.pack(padx=5, pady=5)
# 도착일 프레임 & 콤보박스
arr_day_frame = Frame(choose_frame)
arr_day_frame.pack(side="left", padx=10)
arr_day = Label(arr_day_frame, text="도착일", width=8)
arr_day.pack(padx=5, pady=5)
opt_arr_day = [i for i in range(1, 32)]
cmb_arr_day = ttk.Combobox(arr_day_frame, state="readonly", values=opt_arr_day, width=3)
cmb_arr_day.current(0)
cmb_arr_day.pack(padx=5, pady=5)
# 직항여부 체크박스
direct_var = BooleanVar()
direct_frame = Frame(choose_frame)
direct_frame.pack(side="left", padx=10)
direct = Checkbutton(direct_frame, text="직항", variable=direct_var)
direct.pack()
# 검색 버튼
search_frame = Frame(choose_frame)
search_frame.pack(side="left", padx=10)
search_btn = Button(search_frame, padx=5, pady=5, width=10, text="검색", command=get_calandar)
search_btn.pack()



# 항공권 사이트 라벨 프레임
site_frame = LabelFrame(root, text="항공권 사이트")
site_frame.pack(padx=5, pady=5, ipadx=100, ipady=5)
# 네이버 항공권 버튼
nav_btn = Button(site_frame, padx=5, pady=5, width=12, text="네이버 항공권", state="disabled", command=link_open)
nav_btn.pack()



# 이미지 리스트 라벨 프레임
list_label = LabelFrame(root, text="정확도 상위 5개")
list_label.pack(fill="x", padx=5, pady=5, ipady=3)
# 이미지 리스트 프레임
list_frame = Frame(list_label)
list_frame.pack(fill="both", padx=5, pady=5)
# 이미지 리스트 박스
list_box = Listbox(list_frame, selectmode="extended", width=125, height=5, font=("Courier New", 10))
list_box.pack(fill="both", expand=True)



# 로딩바 라벨 프레임
loading_label = LabelFrame(root, text="로딩 상태")
loading_label.pack(padx=5, pady=5, ipadx=50, ipady=5)
# 로딩바 프레임
loading_frame = Frame(loading_label)
loading_frame.pack(fill="both", padx=5, pady=5)
# 로딩바
loading_bar = ttk.Progressbar(loading_frame, orient="horizontal", mode="indeterminate", length=200)
loading_bar.pack(pady=5)



root.resizable(False, False)
root.mainloop()
