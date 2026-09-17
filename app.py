```python
import streamlit as st
import pandas as pd

# Cấu hình trang
st.set_page_config(
    page_title="Công cụ tính Lãi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

# Hiển thị logo
st.image("Logo.jpg.JPG", width=200)

# Tiêu đề ứng dụng
st.title("💰 Công Cụ Tính Tiền Tiết Kiệm")
st.write(
    "Ứng dụng hỗ trợ tính toán tiền lãi đơn và lãi kép "
    "dựa trên số tiền gửi, thời gian và lãi suất."
)

st.markdown("---")

# Tạo 2 cột để nhập dữ liệu
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
        options=[
            "Hàng tháng",
            "Hàng quý (3 tháng)",
            "Hàng năm (12 tháng)"
        ],
        index=0
    )

# Ánh xạ kỳ hạn ghép lãi sang số tháng
map_ky_han = {
    "Hàng tháng": 1,
    "Hàng quý (3 tháng)": 3,
    "Hàng năm (12 tháng)": 12
}

thang_ghep_lai = map_ky_han[ky_han_ghep_lai]

st.markdown("---")

# Nút thực hiện tính toán
if st.button("🚀 Tính tiền lãi", use_container_width=True):

    # =========================
    # 1. TÍNH LÃI ĐƠN
    # =========================

    lai_don = (
        so_tien_gui
        * (lai_suat_nam / 100 / 12)
        * so_thang
    )

    tong_lai_don = so_tien_gui + lai_don

    # =========================
    # 2. TÍNH LÃI KÉP
    # =========================

    # Số kỳ ghép lãi
    so_ky = so_thang / thang_ghep_lai

    # Lãi suất cho mỗi kỳ
    lai_suat_ky = (
        lai_suat_nam / 100
        * thang_ghep_lai / 12
    )

    # Công thức lãi kép:
    # A = P * (1 + r)^n
    tong_lai_kep = (
        so_tien_gui
        * (1 + lai_suat_ky) ** so_ky
    )

    lai_kep = tong_lai_kep - so_tien_gui

    # Chênh lệch
    chenh_lech_lai = lai_kep - lai_don
    chenh_lech_tong = tong_lai_kep - tong_lai_don

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================

    st.subheader("📌 Kết Quả Dự Tính")

    m1, m2 = st.columns(2)

    # Lãi đơn
    with m1:
        st.subheader("💵 Lãi Đơn")

        st.metric(
            "Tiền lãi nhận được",
            f"{lai_don:,.0f} VNĐ"
        )

        st.metric(
            "Tổng tiền thực nhận",
            f"{tong_lai_don:,.0f} VNĐ"
        )

    # Lãi kép
    with m2:
        st.subheader("📈 Lãi Kép")

        st.metric(
            "Tiền lãi nhận được",
            f"{lai_kep:,.0f} VNĐ",
            delta=f"{chenh_lech_lai:,.0f} VNĐ so với lãi đơn"
        )

        st.metric(
            "Tổng tiền thực nhận",
            f"{tong_lai_kep:,.0f} VNĐ"
        )

    # =========================
    # BẢNG SO SÁNH
    # =========================

    st.markdown("---")
    st.subheader("📊 Bảng So Sánh Chi Tiết")

    data = {
        "Hạng mục": [
            "Số tiền gốc ban đầu",
            "Tổng tiền lãi",
            "Tổng số tiền nhận được"
        ],

        "Lãi Đơn (VNĐ)": [
            f"{so_tien_gui:,.0f}",
            f"{lai_don:,.0f}",
            f"{tong_lai_don:,.0f}"
        ],

        "Lãi Kép (VNĐ)": [
            f"{so_tien_gui:,.0f}",
            f"{lai_kep:,.0f}",
            f"{tong_lai_kep:,.0f}"
        ],

        "Chênh lệch (VNĐ)": [
            "0",
            f"{chenh_lech_lai:,.0f}",
            f"{chenh_lech_tong:,.0f}"
        ]
    }

    df = pd.DataFrame(data)

    st.table(df)

    # =========================
    # THÔNG TIN KHOẢN GỬI
    # =========================

    st.markdown("---")
    st.subheader("📋 Thông Tin Khoản Gửi")

    info1, info2, info3 = st.columns(3)

    with info1:
        st.metric(
            "Tiền gửi",
            f"{so_tien_gui:,.0f} VNĐ"
        )

    with info2:
        st.metric(
            "Thời gian",
            f"{so_thang} tháng"
        )

    with info3:
        st.metric(
            "Lãi suất",
            f"{lai_suat_nam:.1f}%/năm"
        )
```
