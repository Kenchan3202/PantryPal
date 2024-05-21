import barcode_scanning


def test_scan_barcode_file_with_code_present():
    code_list = [barcode_scanning.scan_barcode_file("C:/files/barcode_sample_1.png"),
                 barcode_scanning.scan_barcode_file("C:/files/barcode_sample_2.jpeg"),
                 barcode_scanning.scan_barcode_file("C:/files/barcode_sample_3.jpg"),
                 barcode_scanning.scan_barcode_file("C:/files/barcode_sample_4.webp")]
    if code_list == ["0512345000107", "0896222001044", "5000171010025", "9300633929169"]:
        return "pass"
    else:
        return "fail"


def test_scan_barcode_file_with_code_absent():
    if barcode_scanning.scan_barcode_file("C:/files/absent_barcode_sample.jpg") is None:
        return "pass"
    else:
        return "fail"


def test_scan_barcode_webcam_timeout():
    if barcode_scanning.scan_barcode_webcam(0.1) is None:
        return "pass"
    else:
        return "fail"


print(test_scan_barcode_file_with_code_present(), ": test_scan_barcode_file_with_code_present")
print(test_scan_barcode_file_with_code_absent(), ": test_scan_barcode_file_with_code_absent")
print(test_scan_barcode_webcam_timeout(), ": test_scan_barcode_webcam_timeout")
