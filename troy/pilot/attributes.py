
import inspect

# FIXME: add a tagging 'Monitorable' interface, which enables callbacks.
# FIXME: add a flag to mark attributes as fixed, so that app cannot change flags (type...)
#        also: __delattr__
# FIXME: implement URL parser checks (or Troy URL class, or use some python URL class)
# FIXME: add an instance_data_ attribute registration to all Troy classes, and
#        document usage for adaptor developers.

################################################################################
#
# Callback (Abstract) Class
#
class Callback ():
    """
    Callback base class.

    All stateful objects of the pilot API allow to register a callback for any
    changes of its attributes, such as 'state' and 'state_detail'.  Those
    callbacks can be python call'ables, or derivates of this callback base
    class.  Instances which inherit this base class MUST implement (overload)
    the cb() method.

    The callable, or the callback's cb() method is what is invoked whenever the
    TROY implementation is notified of an change on the monitored object's
    attribute.

    The cb instance receives three parameters upon invocation:

      - member: the watched attribute (e.g. 'state' or 'state_detail')
      - value:  the new value of the watched attribute
      - obj:    the watched object instance

    If the callback returns 'True', it will remain registered after invocation,
    to monitor the attribute for the next subsequent state change.  On returning
    'False' (or nothing), the callback will not be called again.

    To register a callback on a object instance, use::

      class MyCallback (troy.pilot.Callback) :

        def __init__ (self, msg) :
          self.msg_ = msg

        def cb (self, obj, member, value) :
          print " %s\\n %s (%s) : %s"  %  self.msg_, obj, member, value

        def main () :

          cpd = troy.pilot.compute_pilot_description ()
          cps = troy.pilot.compute_pilot_service ()
          cp  = cps.create_pilot (cpd)

          mcb = MyCallback ("Hello Pilot, how is your state?")

          cp.attribute_register_cb ('state', mcb)

    See documentation of the L{Attributes} interface for further details and
    examples.
    """

    def __init__ (self) :
        """ The callback constructor simply raises an IncorrectState exception,
            to signal that the application needs to inherit the callback class
            in a custom class in order to use notifications.
        """
        raise TroyException (Error.IncorrectState,
                             "Callback class must be inherited before use!")


    def cb (self, wu, member, value) :
        """ This is the method that needs to be implemented by the application

            Keyword arguments::

                member: the watched attribute
                value:  the new value of the watched attribute
                obj:    the watched object instance

            Return::

                keep:   bool, signals to keep (True) or remove (False) the callback
                        after invocation

            Callback invocation MAY (and in general will) happen in a separate
            thread -- so the application need to make sure that the callback
            code is thread-safe.

            The boolean return value is used to signal Troy if the callback
            should continue to listen for events (return True) , or if it rather
            should get unregistered after this invocation (return False).
        """
        pass



################################################################################
#
#
#
class Attributes (dict):
    """
    Attribute Interface Class

    The Attributes interface has a very simple API -- it can be used as a Python
    dictionary.  In fact, in inherits from 'dict', and can thus interchangeably
    used.  By overloading the dictionary setter and getter methods it provides,
    however, some additional semantics.

    In particular, a class which uses this interface can internally specify
    which attributes can be set, and what type they have.  Also, default values
    can be specified, and the class provides a rudimentary support for
    converting scalar attributes into vector attributes and back.

    Also, the consumer of this API can register callbacks, which get triggered
    on changes to specific attribute values.

    Example use case::

        class Transliterator ( Attributes ) :

            def __init__ (self) :
                self.attribute_register_   ('apple', 'Appel', self.String, self.Scalar, self.Writeable)
                self.attribute_register_   ('plum',  'Pruim', self.String, self.Scalar, self.ReadOnly)
                self.attribute_extensible_ (True)


        if __name__ == "__main__":

            def cb (key, val, obj) :
                print "called: %s - %s - %s"  %  (key, val, type (obj))

            trans = Transliterator ()

            print " -- apple"
            print trans.apple
            trans.apple = 'Apfel'
            print trans.apple

            trans.attribute_register_cb ('apple', cb)
            trans.apple = 'Apfel'

            .apple = 'Abbel'
            print trans.apple


            print "\\n -- plum"
            print trans.plum
          # trans.plum = 'Pflaume'  # raises exception
            print trans.plum

            print "\\n -- peach"
            print trans.peach       # rases exception
            trans.peach = 'Birne'
            print trans.peach

    This example will result in::

        -- apple
        Appel
        Apfel
        called: apple - Apfel - <class '__main__.Foo'>
        called: apple - Apfel - <class '__main__.Foo'>
        Apfel

         -- plum
        Pruim
        Pruim

         -- peach
        None
        Birne

    Note that using this interface *and* inheriting from Python's dict object
    (or any other base classes which define / overload dictionary setters and
    getters) is probably a bad idea.
    """

    # FIXME: need an internal method to set readonly attributes from within
    # Troy.  That in turn means we have to move the checks/conversions into
    # a separate private routine, to use them consistently for public and
    # private setters.


    ############################################################################
    #
    # define a couple of constants for the attribute API, mostly for registering
    # attributes.
    #
    # type enums
    Any         = 'any'        # any python type can be set
    URL         = 'url'        # URL type (string + URL parser checks)
    Int         = 'int'        # Integer type
    Float       = 'float'      # float type
    String      = 'string'     # string, duh!
    Bool        = 'bool'       # True or False or Maybe
    Enum        = 'enum'       # value is any one of a list of candidates
    Time        = 'time'       # seconds since epoch, or any py time thing
                               # which can be converted into such

    # mode enums
    Writeable   = 'writeable'  # the consumer of the interface can change
                               # the attrib value
    ReadOnly    = 'readonly'   # the consumer of the interface can not
                               # change the attrib value.  The
                               # implementation can still change it.
    Final       = 'final'      # neither consumer nor implementation can
                               # change the value anymore

    # extensible enum
    Extended    = True         # new attributes can be added on the fly
    NotExtended = False        # setting new attributes will raise an exception

    # flavor enums
    Scalar      = 'scalar'     # the attribute value is a single data element
    Vector      = 'vector'     # the attribute value is a list of data elements




    ############################################################################
    #
    #
    #
    def __init__(self):
        """
        This method is not supposed to be directly called by the consumer of
        this API -- it is called indirectly via derived object construction.

        init makes sure that the basic structures are in place on the attribute
        dictionary - this saves us ton of safety checks later on.
        """
        self.attribute_init_ ()


    ############################################################################
    #
    #
    #
    def attribute_init_ (self) :
        """
        This method is not supposed to be directly called by the consumer of
        this API.

        The attribute_init_ method initializes the interface's internal data
        structures.  We always need the attribute dict, and the extensible flag.
        Everything else can be added on the fly.  The method makes not to
        overwrite any settings -- initialization occurs only once!
        """

        if not 'attributes_' in self :
            self['attributes_'] = {}

        if not 'extensible_' in self :
            self['extensible_'] = False


    ############################################################################
    #
    #
    #
    def attribute_extensible_ (self, e=True) :
        """
        Allow (or forbid) the on-the-fly creation of new attributes.
        This method should only be called within derived classes.
        """

        self['extensible_'] = e


    ############################################################################
    #
    #
    #
    def attribute_register_ (self, key, default=None, typ=String, flavor=Scalar, mode=Writeable, ext=False) :
        """
        Register a new attribute.

        This function ignores the extensible, final and readonly flag, and is
        supposed to be used by derived classes, not by the consumer of the API.

        Note that the given attribute will overwrite any previously existing
        attribute w/o warning (even if that one was final).
        """
                # FIXME: check for correct mode and flavor settings

        # make sure interface is ready to use
        self.attribute_init_ ()

        # remove any old instance of this attribute
        self.attribute_unregister_ (key)

        # register the attribute and properties
        self['attributes_'][key]              = {}
        self['attributes_'][key]['value']     = default
        self['attributes_'][key]['default']   = default
        self['attributes_'][key]['type']      = typ
        self['attributes_'][key]['flavor']    = flavor
        self['attributes_'][key]['mode']      = mode
        self['attributes_'][key]['extended']  = ext
        self['attributes_'][key]['callbacks'] = []


    ############################################################################
    #
    #
    #
    def attribute_unregister_ (self, key) :
        """
        Unregister an attribute.

        This function ignores the extensible, final and readonly flag, and is
        supposed to be used by derived classes, not by the consumer of the API.

        Note that unregistering is different from setting the value to 'None' --
        all meta information about the attribute will be removed.

        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        # if the attribute exists, purge it
        if key in self['attributes_'] :
            del (self['attributes_'][key])


    ############################################################################
    #
    #
    #
    def attribute_set_final_ (self, key, val=None) :
        """
        This method will set the 'final' flag for an attribute, signalling that
        the attribute will never change again.  A final value can optionally be
        provided -- otherwise the attribute is frozen with its current value.

        Note that attribute_set_final() will trigger callbacks, if a new value
        is  given.

        This function ignores the readonly flag, and is supposed to be used by
        derived classes, not by the consumer of the API.

        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        # check if we know about that attribute
        if not key in self['attributes_'] :
            raise AttributeError(" attribute %s is not set"  %  key)

        if None == val :
            # freeze at current value unless indicated otherwise
            val = self['attributes_'][key]['value']

        # set the final value, and flag as final.
        self.attribute_set_ (key, val)
        self['attributes_'][key]['mode'] = self.Final


    ############################################################################
    #
    #
    #
    def attribute_set_ (self, key, val=None) :
        """
        This method will set an attribute, irrespectively of its mode.

        if no value is provided, the attribute's value is set to 'None'.  Note
        that attribute_set_() will trigger callbacks, if a new value (different
        from the old value) is given.

        Note that new attributes are silently created, irrespectively of the
        'extensible' flag.

        This function ignores the readonly flag, and is supposed to be used by
        derived classes, not by the consumer of the API.  It should be used to
        change attributes which are marked as 'readonly' to the consumer.
        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        # apply any attribute conversion
        val = self.attribute_conversion_ (key, val)

        self.__setattr__ (key, val)


    ############################################################################
    #
    #
    #
    def attribute_is_final (self, key) :
        """
        This method will query the 'final' flag for an attribute, which signals that
        the attribute will never change again.
        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        # check if we know about that attribute
        if not key in self['attributes_'] :
            raise AttributeError(" attribute %s is not set"  %  key)

        if self.Final == self['attributes_'][key]['mode'] :
             return True

        # no final flag found -- assume non-finality!
        return False

    # FIXME: add other inspection methods (is_string, ..., is, writeable, ...)


    ############################################################################
    #
    #
    #
    def attribute_register_cb (self, key, cb) :
        """
        For any attribute change, the API will check if any callbacks are
        registered for that attribute.  If so, those callbacks will be called
        in order of registration.  This registration function will return an
        id (cookie) identifying the callback -- that id can be used to
        unregister the callback.

        A callback is any callable python construct, and MUST accept three
        arguments::

            - String key: the name of the attribute which changed
            - Any    val: the new value of the attribute
            - Any    obj: the object on which this attribute interface was called

        The 'obj' can be any python object type, but is guaranteed to expose
        this attribute interface.

        The callback SHOULD return 'True' or 'False' -- on 'True', the callback
        will remain registered, and will thus be called again on the next
        attribute change.  On returning 'False', the callback will be
        unregistered, and will thus not be called again.  Returning nothing is
        interpreted as 'False', other return values lead to undefined behavior.

        Note that callbacks will not be called on 'Final' attributes.
        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        if not key in self['attributes_'] :
            raise AttributeError(" attribute %s is not set"  %  key)

        self['attributes_'][key]['callbacks'].append (cb)
        return len (self['attributes_'][key]['callbacks']) - 1


    ############################################################################
    #
    #
    #
    def attribute_unregister_cb (self, key, id=None) :
        """
        This method allows to unregister a previously registered callback, by
        providing its id.  It is not an error to remove a non-existing cb, but
        a valid ID MUST be provided -- otherwise, an AttributeError is raised.

        If no ID is provided (id == None), all callbacks are removed for this
        attribute.
        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        if not key in self['attributes_'] :
            raise AttributeError(" attribute %s is not set"  %  key)

        # id == None: remove all callbacks
        if not id :
            self['attributes_'][key]['callbacks'] = []
        else :
            if len (self['attributes_'][key]['callbacks']) < id :
                raise AttributeError(" invalid callback cookie"  %  key)
            else :
                self['attributes_'][key]['callbacks'][id] = undef


    ############################################################################
    #
    #
    #
    def attribute_call_cb_ (self, key) :
        """
        This internal function is not to be used by the consumer of this API.

        It triggers the invocation of all callbacks for a given attribute.
        Callbacks returning False (or nothing at all) will be unregistered after
        their invocation.
        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        if not key in self['attributes_'] :
            raise AttributeError(" attribute %s is not set"  %  key)

        for id in range (len(self['attributes_'][key]['callbacks'])) :
            cb = self['attributes_'][key]['callbacks'][id]

            ret = False
            if inspect.isclass (cb) and \
               issubclass (cb, Callback) :
                ret = cb.cb (key, self.__get_attr__ (key), self)
            else :
                ret = cb (key, self.__getattr__ (key), self)

            # remove callbacks which return 'False'
            if not ret :
                self.attribute_unregister_cb (key, id)


    ############################################################################
    #
    #
    #
    def __getattr__ (self, key) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is implicitly used via the dictionary interface.

        The getattr method returns the value of the specified attribute.  If
        that attribute does not exist, an AttributeError is raised.  It is not
        an error to query an unset attribute though -- that will result in
        'None' to be returned.

        Note that this method is not performing any checks or conversions --
        those are all performed when *setting* an attribute.  So, any attribute
        flags (type, mode, flavor) are evaluated on setting, not on getting.
        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        if not key in self['attributes_'] :
            raise AttributeError(" attribute %s is not set"  %  key)

        if not 'value' in self['attributes_'][key] :
            return None

        return self['attributes_'][key]['value']


    ############################################################################
    #
    #
    #
    def __setattr__ (self, key, val) :
        """
        This internal method should not be explicitly called by consumers of
        this API, but is implicitly used via the dictionary interface.

        The setattr method sets the value of the specified attribute.  If that
        attribute does not exist, an AttributeError is raised -- unless the
        attribute set is marked 'extensible' -- in that case, the attribute is
        created and set on the fly.  It is not an error to query unset attribute
        though -- that is done by setting it to 'None'.  If a default is
        specified for an attribute, setting 'None' will in fact restore the
        default value.

        Note that this method is performing a number of checks and conversions,
        to match the value type to the attribute flags (type, mode, flavor).
        Those conversions are not guaranteed to yield the expected result -- for
        example, the conversion from 'scalar' to 'vector' is, for complex types,
        ambiguous at best, and very likely stupid.  The consumer of the API
        SHOULD ensure correct attribute values.  The conversions are intended to
        support the most trivial and simple use cases (int to string etc).
        Failed conversions will result in an Attribute Error.

        Note::

            Conversions and checks are incomplete at this point!
            See code documentation (FIXMEs) for details.

        Attempts to set a 'final' attribute are silently ignored.  Attempts to
        set a 'readonly' attribute will result in an AttributeError being
        raised.
        """

        # make sure interface is ready to use
        self.attribute_init_ ()

        # if the key is not known
        if not key in self['attributes_'] :
            if not self['extensible_'] :
                # we cannot add new keys on non-extensible sets
                raise AttributeError(" attribute set is not extensible (key %s)"  %  key)
            else :
                # if the set is extensible, we can register the new key.  It
                # won't have any callbacks at this point.
                self.attribute_register_ (key, val, self.Any, self.Scalar, self.Writeable, self.Extended)

        # known attribute - attempt to set if
        else:

            # check if we are allowed to change the attribute - complain if not.
            # Also, simply ignore write attempts to finalized keys.
            if 'mode' in  self['attributes_'][key] :

                mode = self['attributes_'][key]['mode']

                if   self.Final == mode :
                    return
                elif self.Writeable != mode :
                    raise AttributeError(" attribute %s is not writeable"  %  key)

            val = self.attribute_conversion_ (key, val)

            # make sure the later comparison if does not throw
            if not 'value' in self['attributes_'][key] :
                self['attributes_'][key]['value'] = None

            # only actually change the attribute when the new value differs --
            # and only then invoke any callbacks.
            if val != self['attributes_'][key]['value'] :
                self['attributes_'][key]['value'] = val
                self.attribute_call_cb_ (key)



    ###########################################################################
    #
    #
    #
    def attribute_conversion_ (self, key, val) :
        """
        This is an internal method, and should not be called outside this
        interface implementation.

        The method checks a given attribute value against the attribute's
        flags, and performs some simple type conversion as needed.  Also, the
        method will restore a 'None' value to the attribute's default value.
        """
        # make sure interface is ready to use
        self.attribute_init_ ()

        # if the key is not known
        if not key in self['attributes_'] :
            # cannot handle unknown attributes
            return val

        # check if a value is given.  If not, revert to the default value
        # (if available)
        if val == None :
            if 'default' in self['attributes_'][key] :
                val = self['attributes_'][key]['default']


        # check if the value has the correct flavor - if not, attempt to
        # convert
        # FIXME: there are certainly nicer and more reversible ways to
        #        convert the flavors...
        if 'flavor' in  self['attributes_'][key] :

            flavor = self['attributes_'][key]['flavor']

            # wrap value into a list if needed
            # TODO: consider splitting strings?
            if flavor == self.Vector and not isinstance (val, list) :
                val = [val]

            # serialize list into scalar (string)
            if flavor == self.Scalar and isinstance (val, list) :
                val = str(val)


        # FIXME: along the same lines, we could attempt some type
        #        conversions...

        return val

################################################################################

