# ================================================================
# ||                        TUGAS BESAR                         ||
# ================================================================
# || Kelompok: 7                                                ||
# || Judul   : Split Bill Kost/Keluarga (Decimal,CLI)           ||
# || Anggota : 1. Romeo Lando Wero Panggabean   (2410631160035) ||
# ||           2. Muhammad Rizqi Utomo          (2410631160081) ||
# ||           2. Arrauf Choirul Susanto        (2410631160005) ||
# ||           3. Muhammad Fauzan               (2410631160076) ||
# ================================================================


#!/usr/bin/env python3
import argparse
import sys
from decimal import Decimal, InvalidOperation, getcontext, ROUND_HALF_UP

# Presisi internal; pembulatan uang eksplisit ke 2 desimal
getcontext().prec = 28
CENT = Decimal("0.01")

def to_decimal(s: str) -> Decimal:
    """Bersihkan input angka (hilangkan koma/space ribuan), lalu konversi ke Decimal."""
    if s is None:
        raise InvalidOperation("None")
    cleaned = s.replace(",", "").replace(" ", "")
    return Decimal(cleaned)

def format_rupiah(d: Decimal) -> str:
    q = d.quantize(CENT, rounding=ROUND_HALF_UP)
    # format with dot as thousand separator, comma as decimal not desired; use replace trick
    s = f"{q:,.2f}".replace(",", ".")
    return f"Rp {s}"

def interactive_mode():
    """Mode interaktif jika argumen CLI tidak lengkap."""
    print("=== MODE INTERAKTIF: Input data pembagian kos ===")
    try:
        n_raw = input("Masukkan jumlah orang: ").strip()
        n = int(n_raw)
        if n <= 0:
            print("❌ Jumlah orang harus > 0")
            sys.exit(1)
    except (ValueError, EOFError, KeyboardInterrupt):
        print("❌ Input jumlah orang tidak valid. Dibatalkan.")
        sys.exit(1)

    names = []
    contributions = []
    print("\nMasukkan data tiap orang (satu per satu):")
    for i in range(n):
        try:
            nama = input(f"Nama orang ke-{i+1}: ").strip()
            bayar_raw = input(f"Kontribusi {nama} (tanpa pemisah ribuan, contoh 200000 atau 200000.50): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDibatalkan.")
            sys.exit(1)

        if not nama:
            print("❌ Nama tidak boleh kosong.")
            sys.exit(1)
        try:
            bayar = to_decimal(bayar_raw)
            if bayar < 0:
                raise InvalidOperation("neg")
        except InvalidOperation:
            print(f"❌ Nilai kontribusi '{bayar_raw}' tidak valid.")
            sys.exit(1)

        names.append(nama)
        contributions.append(bayar)

    # total tagihan: tanyakan explicit
    try:
        total_raw = input("\nMasukkan TOTAL tagihan kos (contoh 1000000): ").strip()
        total_tagihan = to_decimal(total_raw)
        if total_tagihan < 0:
            raise InvalidOperation("neg")
    except (InvalidOperation, EOFError, KeyboardInterrupt):
        print("❌ Total tagihan tidak valid. Dibatalkan.")
        sys.exit(1)

    return names, contributions, total_tagihan

def cli_mode(args):
    """Mode CLI: ambil dari argparse. Jika --total tidak diberikan, gunakan sum(pay)."""
    # names and pay must be same length
    names = args.names
    pays = args.pay
    if len(names) != len(pays):
        print("❌ ERROR: Jumlah nama dan jumlah kontribusi (--names / --pay) harus sama.")
        sys.exit(1)

    try:
        contributions = [to_decimal(p) for p in pays]
    except InvalidOperation:
        print("❌ ERROR: Salah satu nilai kontribusi tidak valid.")
        sys.exit(1)

    # total: bisa diberikan oleh --total, atau dihitung otomatis dari sum(contributions)
    if args.total is not None:
        try:
            total_tagihan = to_decimal(args.total)
        except InvalidOperation:
            print("❌ ERROR: Nilai --total tidak valid.")
            sys.exit(1)
    else:
        total_tagihan = sum(contributions)

    return names, contributions, total_tagihan

def main():
    parser = argparse.ArgumentParser(
        description="Split bill kos/keluarga — Decimal + CLI. Jika argumen tidak lengkap, masuk mode interaktif."
    )
    parser.add_argument("--names", nargs="+", help="Nama tiap orang (contoh: --names A B C)")
    parser.add_argument("--pay", nargs="+", help="Kontribusi tiap orang (contoh: --pay 200000 300000 500000)")
    parser.add_argument("--total", help="Total tagihan (opsional; jika tidak ada, akan digunakan sum kontribusi)")

    args = parser.parse_args()

    # Jika argumen CLI lengkap (names dan pay diberikan), gunakan cli_mode.
    # Jika tidak, jangan biarkan argparse mem-error — masuk ke interactive_mode.
    if args.names and args.pay:
        names, contributions, total_tagihan = cli_mode(args)
    else:
        names, contributions, total_tagihan = interactive_mode()

    n = len(names)
    if n == 0:
        print("❌ Tidak ada data nama.")
        sys.exit(1)

    # Hitung rata-rata porsi berdasarkan total_tagihan yang diberikan
    rata_exact = (total_tagihan / Decimal(n))
    rata_2d = rata_exact.quantize(CENT, rounding=ROUND_HALF_UP)
    residual = total_tagihan - (rata_2d * n)

    total_contrib = sum(contributions)

    print("\n" + "=" * 70)
    print("              HASIL SPLIT BILL KOS/KELUARGA (Decimal + CLI)")
    print("=" * 70)
    print(f"Total Tagihan        : {format_rupiah(total_tagihan)}")
    print(f"Jumlah Orang         : {n}")
    print(f"Porsi rata (tepat)   : {rata_exact} (internal)")
    print(f"Porsi rata (uang)    : {format_rupiah(rata_2d)}")
    print(f"Residual pembulatan  : {format_rupiah(residual)}")
    print("-" * 70)
    print("Rincian per orang (Kontribusi vs Porsi rata):")
    print("-" * 70)

    for i, name in enumerate(names):
        contrib = contributions[i]
        selisih = (contrib - rata_2d).quantize(CENT, rounding=ROUND_HALF_UP)
        if selisih > 0:
            status = f"TERIMA {format_rupiah(selisih)}"
        elif selisih < 0:
            status = f"BAYAR  {format_rupiah(-selisih)}"
        else:
            status = "PAS"
        print(f"{name:<18} | Bayar: {format_rupiah(contrib):<18} | {status}")

    print("-" * 70)
    # Cek apakah total kontribusi cukup terhadap total_tagihan
    if total_contrib > total_tagihan:
        print(f"Ada KELEBIHAN total kontribusi sebesar: {format_rupiah(total_contrib - total_tagihan)}")
    elif total_contrib < total_tagihan:
        print(f"Masih KURANG total kontribusi sebesar: {format_rupiah(total_tagihan - total_contrib)}")
    else:
        print("Total kontribusi PAS sama dengan total tagihan.")

    # Jika residual != 0 berikan catatan
    if residual != Decimal("0.00"):
        print("\nCatatan: Residual akibat pembulatan porsi rata tidak nol.")
        print("Jika ingin, program bisa mendistribusikan residual (+0.01) ke beberapa orang agar total pas.")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
    