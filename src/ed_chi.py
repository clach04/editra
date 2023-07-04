# ed_chi.py
# Tombo CHI file io

import ed_txt

import chi_io  # from PyTombo


class EdFileTombo(ed_txt.EdFile):
    pass

    def DoOpen(self, mode):
        """Opens and creates the internal file object
        @param mode: mode to open file in
        @return: True if opened, False if not
        @postcondition: self._handle is set to the open handle

        """
        if not len(self._path):
            return False

        try:
            print(self.__class__)  # ed_txt.EdFile
            print(self.__class__.__name__)  # EdFile
            if self._path.lower().endswith('.chi'):
                if mode == 'rb':
                    # hack time - attempt to support Tombo encrypted files http://tombo.osdn.jp/En/
                    # TODO pickup password from a file, password safe, https://pypi.org/project/keyring/
                    #import getpass
                    #password = getpass.getpass("Password: ")
                    import wx
                    #password = wx.GetTextFromUser("Password (warning visible): ", "Password required")
                    password = wx.GetPasswordFromUser("Password: ", "Password required")
                    #password = 'mypassword'  # DEBUG hard coded password.
                    password = password.encode('us-ascii')

                    fileptr = open(self._path, mode)
                    plain_text = chi_io.read_encrypted_file(fileptr, password)
                    try:
                        file_h = chi_io.FakeFile(plain_text)
                    except chi_io.ChiIO, msg:
                        # FIXME raise IOError()
                        self.SetLastError(unicode(msg))
                        return False
                    finally:
                        fileptr.close()
                        del(password)
                else:
                    # FIXME raise IOError()
                    self.SetLastError(unicode('mode %r not supported for Tombo chi files.' % mode))
            else:
                # FIXME call super instead
                file_h = open(self._path, mode)
        except (IOError, OSError), msg:
            self.SetLastError(unicode(msg))
            return False
        else:
            self._handle = file_h
            self.open = True
            return True

