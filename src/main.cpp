#include <pybind11/pybind11.h>
#include "boost/date_time/gregorian/gregorian.hpp"

int add(int i, int j) {
    return i + j;
}

std::string current_iso_date() {
    auto current_date = boost::gregorian::day_clock::local_day();
    return boost::gregorian::to_iso_extended_string(current_date);
}

namespace py = pybind11;

PYBIND11_MODULE(python_cpp_skel, m) {
    m.doc() = R"pbdoc(
        Pybind11 example plugin
        -----------------------

        .. currentmodule:: python_example

        .. autosummary::
           :toctree: _generate

           add
           subtract
    )pbdoc";

    m.def("add", &add, R"pbdoc(
        Add two numbers

        Some other explanation about the add function.
    )pbdoc");

    m.def("subtract", [](int i, int j) { return i - j; }, R"pbdoc(
        Subtract two numbers

        Some other explanation about the subtract function.
    )pbdoc");

    m.def("date", &current_iso_date, R"pbdoc(
        Returns the current local iso formated date
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}
