import unittest

class UserProfileTestCase(unittest.TestCase):

    def tearDown(self):
        from gravita import user_profile
        user_profile.clear_all()

    def test_unique_id(self):
        from gravita.user_profile import UserProfile
        ids = set()
        for i in range(500):
            up = UserProfile()
            self.assertEqual(up.game, None)
            self.assertTrue(up.name)
            print up.name
            self.assertTrue(up.profile_id)
            self.assertTrue(isinstance(up.profile_id, str))
            self.assertTrue(up.profile_id not in ids)
            ids.add(up.profile_id)

    def test_load_profile(self):
        from gravita.user_profile import UserProfile
        ups = [UserProfile() for i in range(10)]
        for i, p in enumerate(up for up in ups):
            self.assertTrue(UserProfile.load(p.profile_id) is ups[i])

    def test_load_profile_wrong_id(self):
        from gravita.user_profile import UserProfile
        self.assertRaises(KeyError, UserProfile.load, 'flombom')
        


