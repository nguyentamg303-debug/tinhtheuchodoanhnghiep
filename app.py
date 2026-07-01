import streamlit as st

# Cấu hình trang web của ứng dụng
st.set_page_config(page_title="App Tính Chi Phí Nhân Sự Cho Doanh Nghiệp 2026", page_icon="🏢", layout="centered")

# --- CHÈN LOGO THEO FILE TRỰC TIẾP ---
st.image("logo.jpg")

# --- THÔNG TIN THÀNH VIÊN VÀ ĐỀ TÀI ---
st.markdown("### 📝 **Nguyễn Minh Tâm**")
st.title("🏢 Ứng Dụng Tính Chi Phí Nhân Sự & Bảo Hiểm Cho NSDLĐ")
st.write("Quản lý và tối ưu quỹ lương, tính toán nghĩa vụ đóng bảo hiểm của Doanh nghiệp theo luật năm 2026")
st.markdown("---")

# --- PHẦN NHẬP DỮ LIỆU ĐẦU VÀO ---
st.subheader("📋 Nhập thông tin quỹ lương tháng của nhân viên")
gross_salary = st.number_input("1. Mức lương chính ký hợp đồng / Đóng BHXH (VND):", min_value=0, value=30000000, step=500000, format="%d")
bonus_pay = st.number_input("2. Tiền thưởng / Bonus chi trả trong tháng (VND):", min_value=0, value=0, step=500000, format="%d")
overtime_pay = st.number_input("3. Tiền lương tăng ca / làm thêm giờ (VND):", min_value=0, value=0, step=500000, format="%d")

st.markdown("**4. Các khoản phụ cấp, phúc lợi hỗ trợ nhân viên:**")
col_sub1, col_sub2 = st.columns(2)
with col_sub1:
    lunch_allowance = st.number_input("Phụ cấp ăn trưa (VND):", min_value=0, value=0, step=50000)
with col_sub2:
    other_allowance = st.number_input("Phụ cấp khác (Điện thoại, xăng xe, nhà ở) (VND):", min_value=0, value=0, step=50000)

st.markdown("---")

# --- HÀM LOGIC TÍNH TOÁN CHI PHÍ CHO DOANH NGHIỆP ---
def tinh_chi_phi_nsdld(gross, bonus, overtime, lunch, other):
    # Tổng quỹ lương trực tiếp trả cho Người lao động
    direct_salary_cost = gross + bonus + overtime + lunch + other
    
    # Tính các khoản bảo hiểm bắt buộc trích từ quỹ của Doanh nghiệp (Tổng 21.5%)
    nsdld_bhxh_huu_tri = gross * 0.14       # Hưu trí, tử tuất (14%)
    nsdld_bhxh_om_thai = gross * 0.03       # Ốm đau, thai sản (3%)
    nsdld_bhxh_tnld = gross * 0.005         # Tai nạn lao động, bệnh nghề nghiệp (0.5%)
    nsdld_bhtn = gross * 0.01               # Bảo hiểm thất nghiệp (1%)
    nsdld_bhyt = gross * 0.03               # Bảo hiểm y tế (3%)
    
    total_nsdld_insurance = nsdld_bhxh_huu_tri + nsdld_bhxh_om_thai + nsdld_bhxh_tnld + nsdld_bhtn + nsdld_bhyt
    
    # Tổng chi phí thực tế Doanh nghiệp phải gánh chịu cho vị trí nhân sự này
    total_corporate_cost = direct_salary_cost + total_nsdld_insurance
    
    return {
        "direct_salary_cost": direct_salary_cost,
        "bhxh_huu_tri": nsdld_bhxh_huu_tri,
        "bhxh_om_thai": nsdld_bhxh_om_thai,
        "bhxh_tnld": nsdld_bhxh_tnld,
        "bhtn": nsdld_bhtn,
        "bhyt": nsdld_bhyt,
        "total_nsdld_insurance": total_nsdld_insurance,
        "total_corporate_cost": total_corporate_cost
    }

# --- PHẦN NÚT BẤM KÍCH HOẠT VÀ HIỂN THỊ KẾT QUẢ ---
if st.button("🏢 Tính Toán Chi Phí Doanh Nghiệp", type="primary"):
    res = tinh_chi_phi_nsdld(gross_salary, bonus_pay, overtime_pay, lunch_allowance, other_allowance)
    st.markdown("---")
    st.subheader("🎯 Tổng Hợp Chi Phí Nhân Sự (Tổng Doanh Nghiệp Chi)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Tổng lương + phụ cấp trả trực tiếp cho NLĐ", value=f"{res['direct_salary_cost']:,.0f} VND")
        st.metric(label="Tổng tiền bảo hiểm NSDLĐ phải đóng (21.5%)", value=f"{res['total_nsdld_insurance']:,.0f} VND")
    with col2:
        st.metric(label="TỔNG CHI PHÍ THỰC TẾ CỦA DOANH NGHIỆP", value=f"{res['total_corporate_cost']:,.0f} VND")
        
    st.markdown("---")
    st.subheader("📜 Bảng Giải Trình Nghĩa Vụ Trích Đóng Bảo Hiểm Của Doanh Nghiệp")
    
    # Tạo bảng dữ liệu chi tiết cấu trúc bảo hiểm để DN dễ theo dõi và hạch toán kế toán
    insurance_data = [
        {"Hạng mục trích đóng", "Tỷ lệ áp dụng", "Số tiền đóng (VND)"},
        {"Bảo hiểm Xã hội (Hưu trí, Tử tuất)", "14.0%", f"{res['bhxh_huu_tri']:,.0f} VND"},
        {"Bảo hiểm Xã hội (Ốm đau, Thai sản)", "3.0%", f"{res['bhxh_om_thai']:,.0f} VND"},
        {"Bảo hiểm TNLĐ - BNN", "0.5%", f"{res['bhxh_tnld']:,.0f} VND"},
        {"Bảo hiểm Y tế (BHYT)", "3.0%", f"{res['bhyt']:,.0f} VND"},
        {"Bảo hiểm Thất nghiệp (BHTN)", "1.0%", f"{res['bhtn']:,.0f} VND"},
    ]
    
    st.table(insurance_data)
    
    st.info("💡 **Lưu ý kế toán:** Tổng chi phí thực tế của doanh nghiệp (Total Cost) là cơ sở để lập ngân sách nhân sự và tính toán chi phí được trừ khi xác định thuế Thu nhập Doanh nghiệp (TNDN).")
