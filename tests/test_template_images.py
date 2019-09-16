import xcv.template_load

def test_template_image_load():
    assert Path('xcv/templates').is_dir()

def test_template_image_load_my_team_badge():
    assert Path('xcv/templates/myTeamBadge.jpy').is_file()