// sol2

// The MIT License (MIT)

// Copyright (c) 2013-2022 Rapptz, ThePhD and contributors

// Permission is hereby granted, free of charge, to any person obtaining a copy of
// this software and associated documentation files (the "Software"), to deal in
// the Software without restriction, including without limitation the rights to
// use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
// the Software, and to permit persons to whom the Software is furnished to do so,
// subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

#include <catch2/catch_all.hpp>
#include <sol/sol.hpp>

#include <map>
#include <string>

TEST_CASE("containers/associative pairs visits every entry", "associative container iteration reaches the sentinel") {
	sol::state lua;
	lua.open_libraries(sol::lib::base);

	std::map<std::string, int> values { { "first", 1 }, { "second", 2 }, { "third", 3 } };
	lua["values"] = &values;

#if SOL_LUA_VERSION_I_ > 501
	auto result = lua.safe_script(R"(
iteration_count = 0
iteration_sum = 0
for key, value in pairs(values) do
	assert(values[key] == value)
	iteration_count = iteration_count + 1
	iteration_sum = iteration_sum + value
end
)",
	     sol::script_pass_on_error);
#else
	auto result = lua.safe_script(R"(
iteration_count = 0
iteration_sum = 0
local container_pairs = getmetatable(values).__pairs
for key, value in container_pairs(values) do
	assert(values[key] == value)
	iteration_count = iteration_count + 1
	iteration_sum = iteration_sum + value
end
)",
	     sol::script_pass_on_error);
#endif

	REQUIRE(result.valid());
	REQUIRE(lua["iteration_count"].get<std::size_t>() == values.size());
	REQUIRE(lua["iteration_sum"].get<int>() == 6);
}
