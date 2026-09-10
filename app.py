import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(
    page_title="Công cụ tính Lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# Tiêu đề ứng dụng
st.title("💰 Công Cụ Tính Tiền Tiết Kiệm")
st.write("Ứng dụng hỗ trợ tính toán tiền lãi đơn và lãi kép dựa trên số tiền gửi, thời gian và lãi suất.")

st.markdown("---")

# Tạo 2 cột để nhập dữ liệu cho gọn gàng
col1, col2 = st.columns(2)

with col1:
    so_tien_gui = st.number_input(
        "Nhập số tiền gửi (VNĐ):",
        min_value=0.0,
        value=10000000.0,
        step=1000000.0,
        format="%.0f"
    )
    so_thang = st.number_input(
        "Nhập số tháng gửi:",
        min_value=1,
        value=12,
        step=1
    )

with col2:
    lai_suat_nam = st.number_input(
        "Lãi suất (%/năm):",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
        format="%.1f"
    )
    ky_han_ghep_lai = st.selectbox(
        "Tần suất nhập gốc (Cho Lãi kép):",
        options=["Hàng tháng", "Hàng quý (3 tháng)", "Hàng năm (12 tháng)"],
        index=0
    )

# Ánh ánh kỳ hạn ghép lãi sang số tháng
map_ky_han = {
    "Hàng tháng": 1,
    "Hàng quý (3 tháng)": 3,
    "Hàng năm (12 tháng)": 12
}
thang_ghep_lai = map_ky_han[ky_han_ghep_lai]

st.markdown("---")

# Nút thực hiện tính toán
if st.button("🚀 Tính tiền lãi", use_container_width=True):
    # 1. Tính Lãi Đơn
    # Công thức: Lãi = Gốc * (Lãi suất năm / 12) * Số tháng
    lai_don = so_tien_gui * (lai_suat_nam / 100 / 12) * so_thang
    tong_lai_don = so_tien_gui + lai_don

    # 2. Tính Lãi Kép
    # Số kỳ ghép lãi trong 1 năm (n)
    n = 12 / thang_ghep_lai
    # Tổng số năm gửi (t)
    t = so_thang / 12
    # Lãi suất theo kỳ ghép lãi (r / n)
    r_ky = (lai_suat_nam / 100) / n
    # Tổng số kỳ ghép lãi
    tong_so_ky = n * t

    tong_lai_kep = so_tien_gui * ((1 + r_ky) ** tong_so_ky)
    lai_kep = tong_lai_kep - so_tien_gui

    # Hiển thị kết quả tổng quan bằng st.metric
    st.subheader("📌 Kết Quả Dự Tính")
    m1, m2 = st.columns(2)
    
    with m1:
        st.subheader("Lãi Đơn")
        st.metric("Tiền lãi nhận được", f"{lai_don:,.0f} VNĐ")
        st.metric("Tổng tiền thực nhận", f"{tong_lai_don:,.0f} VNĐ")

    with m2:
        st.subheader("Lãi Kép")
        st.metric("Tiền lãi nhận được", f"{lai_kep:,.0f} VNĐ", delta=f"+{lai_kep - lai_don:,.0f} VNĐ (so với lãi đơn)")
        st.metric("Tổng tiền thực nhận", f"{tong_lai_kep:,.0f} VNĐ")

    # Bảng chi tiết so sánh
    st.markdown("---")
    st.subheader("📊 Bảng So Sánh Chi Tiết")
    
    data = {
        "Hạng mục": ["Số tiền gốc ban đầu", "Tổng tiền lãi", "Tổng số tiền nhận được"],
        "Lãi Đơn (VNĐ)": [f"{so_tien_gui:,.0f}", f"{lai_don:,.0f}", f"{tong_lai_don:,.0f}"],
        "Lãi Kép (VNĐ)": [f"{so_tien_gui:,.0f}", f"{lai_kep:,.0f}", f"{tong_lai_kep:,.0f}"],
        "Chênh lệch (VNĐ)": ["0", f"{lai_kep - lai_don:,.0f}", f"{tong_lai_kep - tong_lai_don:,.0f}"]
    }
    
    df = pd.DataFrame(data)
    st.table(df)
