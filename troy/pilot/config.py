
########################################################################
#
#
#
class Config_ (object) :
    """
    The Config class acts, as the name suggests, as a configuration point for
    the Troy implementation.  It hosts a number of Class variables, which
    correspond to different compile and runtime settings for Troy::

      - 'UseAttributes':
          - see L{troy.pilot.Attributes}: enable (True) or disable (False)
            type and key checks for attribute settings on the various Troy
            classes.
          - type   : boolean
          - default: True
          FIXME: not implemented

    """

    UseAttributes = True
    """ use the attribute interface type checks """

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

