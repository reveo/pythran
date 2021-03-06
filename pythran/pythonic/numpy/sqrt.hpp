#ifndef PYTHONIC_NUMPY_SQRT_HPP
#define PYTHONIC_NUMPY_SQRT_HPP

#include "pythonic/include/numpy/sqrt.hpp"

#include "pythonic/utils/functor.hpp"
#include "pythonic/types/ndarray.hpp"
#include "pythonic/utils/numpy_traits.hpp"

namespace pythonic
{

  namespace numpy
  {
#define NUMPY_NARY_FUNC_NAME sqrt
#define NUMPY_NARY_FUNC_SYM boost::simd::sqrt
#include "pythonic/types/numpy_nary_expr.hpp"
  }
}

#endif
