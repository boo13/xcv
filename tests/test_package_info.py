def test_package_info():
    import xcv
    from xcv.version import XCV_VERSION

    assert XCV_VERSION == "0.1.3"
    assert xcv.__email__ == "boo13bot@gmail.com"
    assert xcv.__author__ == "Boo13"
