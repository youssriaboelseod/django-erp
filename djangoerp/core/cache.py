#!/usr/bin/env python
"""This file is part of the django ERP project.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

__author__ = 'Emanuele Bertoldi <emanuele.bertoldi@gmail.com>'
__copyright__ = 'Copyright (c) 2013-2015, django ERP Team'
__version__ = '0.0.5'


from django.contrib.auth.models import AnonymousUser
from .singleton import Singleton


class LoggedInUserCache(metaclass=Singleton):
    """Stores the current user as a member attribute of a singleton.
    
    WARNING: if you manually change the value of "LoggedInUserCanche.user"
    property for your special purposes, remember to restore it on its previous
    value at the end of your special code block. i.e.:

    >> logged_cache = LoggedInUserCache()
    >> current_user = logged_cache.user # Save the previous value!
    >> logged_cache.user = my_specific_needs_user
    >> # ... code ... #
    >> logged_cache.user = current_user # Restore the value!
    """

    user = AnonymousUser()

    def set_user(self, request):
        self.user = request.user
        if not self.user:
            self.clear()
            
    def clear(self):
        self.user = AnonymousUser()

    @property
    def has_user(self):
        return self.user and self.user.is_authenticated
