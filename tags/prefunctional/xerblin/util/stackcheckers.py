'''
Stack Checker Mixins
'''


NUMBER_TYPES = int, float, long


# This is a sort of abstract base class for Stack Checker Mixins.
# It ensures that the super() calls will always succeed.
class _urMixin(object):
    def _stackok(self, stack):
        pass


# Helper for correct pluralization.
_plural = lambda n: ('', 's')[n > 1]


def StackLen(n, cache={}):
    '''
    Return a stack length checker Mixin that checks that at least n items
    are on the stack.
    '''
    assert n > 0

    C = cache.get(n)

    if C: return C

    class StackLenMixin(_urMixin):
        def _stackok(self, stack):
            assert len(stack) >= n, (
                'stack too small, needs %i thing%s' % (n, _plural(n))
                )
            super(StackLenMixin, self)._stackok(stack)

    cache[n] = StackLenMixin

    return StackLenMixin


def StackType(index, type_, cache={}):
    '''
    Return a stack item type checker Mixin that checks that the item at
    index is of type type_.
    '''

    sig = (index, type_)

    C = cache.get(sig)

    if C: return C

    class StackTypeMixin(_urMixin):
        def _stackok(self, stack):
            assert isinstance(stack[index], type_), (
                "stack[%i] isn't %s" % sig
                )
            super(StackTypeMixin, self)._stackok(stack)

    cache[sig] = StackTypeMixin

    return StackTypeMixin


def StackHasAttr(index, attr, cache={}):
    '''
    Return a stack item checker Mixin that checks that the item at index
    has an attribute named attr.
    '''

    assert isinstance(attr, basestring)

    sig = (index, attr)

    C = cache.get(sig)

    if C: return C

    class StackHasAttrMixin(_urMixin):
        def _stackok(self, stack):
            assert hasattr(stack[index], attr), (
                'stack[%i] has no %s attribute' % sig
                )
            super(StackHasAttrMixin, self)._stackok(stack)

    cache[sig] = StackHasAttrMixin

    return StackHasAttrMixin


if __name__ == '__main__':
    class S(
        StackLen(2),
        StackType(0, int),
        StackType(1, basestring)
        ):
        pass

    s = S()
    s._stackok([2, '1'])
    s._stackok([1, 2])
