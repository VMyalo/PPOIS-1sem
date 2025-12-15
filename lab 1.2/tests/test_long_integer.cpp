// tests/test_long_integer.cpp
#include "long_integer.h"
#include <UnitTest++/UnitTest++.h>
#include <sstream>
#include <string>

static std::string toString(const LongInteger& num) {
    std::ostringstream oss;
    oss << num;
    return oss.str();
}

SUITE(LongIntegerTests) {

TEST(DefaultConstructor) {
    LongInteger num;
    CHECK_EQUAL("0", toString(num));
}

TEST(ConstructorFromStringBasic) {
    LongInteger pos("123");
    LongInteger neg("-456");
    LongInteger zero("0");
    LongInteger plus("+789");

    CHECK_EQUAL("123", toString(pos));
    CHECK_EQUAL("-456", toString(neg));
    CHECK_EQUAL("0", toString(zero));
    CHECK_EQUAL("789", toString(plus));
}

TEST(ConstructorFromStringEdgeCases) {
    LongInteger leading_zeros("000123");
    LongInteger neg_leading_zeros("-000456");
    LongInteger zero_with_signs("+0");
    LongInteger neg_zero("-0");

    CHECK_EQUAL("123", toString(leading_zeros));
    CHECK_EQUAL("-456", toString(neg_leading_zeros));
    CHECK_EQUAL("0", toString(zero_with_signs));
    CHECK_EQUAL("0", toString(neg_zero));
}

TEST(ConstructorFromStringInvalid) {
    CHECK_THROW(LongInteger(""), std::invalid_argument);
    CHECK_THROW(LongInteger("abc"), std::invalid_argument);
    CHECK_THROW(LongInteger("-"), std::invalid_argument);
    CHECK_THROW(LongInteger("+"), std::invalid_argument);
    CHECK_THROW(LongInteger("12-34"), std::invalid_argument);
    CHECK_THROW(LongInteger("++123"), std::invalid_argument);
}

TEST(CopyConstructor) {
    LongInteger original("-98765432109876543210");
    LongInteger copy(original);
    CHECK(original == copy);
}

TEST(AssignmentOperator) {
    LongInteger a("12345");
    LongInteger b;
    b = a;
    CHECK(a == b);
}

TEST(EqualityAndInequality) {
    LongInteger a("123");
    LongInteger b("123");
    LongInteger c("456");
    CHECK(a == b);
    CHECK(a != c);
}

TEST(ComparisonOperators) {
    LongInteger a("100");
    LongInteger b("200");
    LongInteger neg_a("-100");
    LongInteger neg_b("-200");
    LongInteger zero("0");

    CHECK(a < b);
    CHECK(b > a);
    CHECK(neg_b < neg_a);
    CHECK(neg_a > neg_b);
    CHECK(zero < LongInteger("1"));
    CHECK(zero > LongInteger("-1"));
}

TEST(AdditionSameSign) {
    LongInteger a("123");
    LongInteger b("456");
    CHECK_EQUAL("579", toString(a + b));

    LongInteger neg_a("-123");
    LongInteger neg_b("-456");
    CHECK_EQUAL("-579", toString(neg_a + neg_b));
}

TEST(AdditionDifferentSign) {
    CHECK_EQUAL("300", toString(LongInteger("500") + LongInteger("-200")));
    CHECK_EQUAL("-300", toString(LongInteger("200") + LongInteger("-500")));
    CHECK((LongInteger("123") + LongInteger("-123")) == LongInteger("0"));
}

TEST(AdditionLargeNumbers) {
    LongInteger a("999999999999999999999999999999");
    LongInteger b("1");
    CHECK_EQUAL("1000000000000000000000000000000", toString(a + b));
}

TEST(SubtractionBasic) {
    CHECK_EQUAL("300", toString(LongInteger("500") - LongInteger("200")));
    CHECK_EQUAL("-300", toString(LongInteger("-500") - LongInteger("-200")));
    CHECK_EQUAL("700", toString(LongInteger("200") - LongInteger("-500")));
}

TEST(MultiplicationBasic) {
    CHECK_EQUAL("408", toString(LongInteger("12") * LongInteger("34")));
    CHECK_EQUAL("-408", toString(LongInteger("-12") * LongInteger("34")));
    CHECK((LongInteger("0") * LongInteger("99999999999")) == LongInteger("0"));
}

TEST(MultiplicationLarge) {
    LongInteger a("123456789");
    LongInteger b("987654321");
    CHECK_EQUAL("121932631112635269", toString(a * b));
}

TEST(DivisionBasic) {
    CHECK((LongInteger("100") / LongInteger("10")) == LongInteger("10"));
    CHECK((LongInteger("-100") / LongInteger("10")) == LongInteger("-10"));
    CHECK((LongInteger("10") / LongInteger("3")) == LongInteger("3"));
}

TEST(ModuloBasic) {
    CHECK((LongInteger("10") % LongInteger("3")) == LongInteger("1"));
    CHECK((LongInteger("-10") % LongInteger("3")) == LongInteger("-1"));
    CHECK((LongInteger("10") % LongInteger("-3")) == LongInteger("1"));
}

TEST(DivisionByZero) {
    LongInteger a("100");
    LongInteger b("0");
    CHECK_THROW(a / b, std::domain_error);
    CHECK_THROW(a % b, std::domain_error);
}

TEST(CompoundAssignment) {
    LongInteger a("10");
    a += LongInteger("5");
    CHECK(a == LongInteger("15"));
    a -= LongInteger("3");
    CHECK(a == LongInteger("12"));
    a *= LongInteger("2");
    CHECK(a == LongInteger("24"));
    a /= LongInteger("3");
    CHECK(a == LongInteger("8"));
    a %= LongInteger("5");
    CHECK(a == LongInteger("3"));
}

TEST(PreIncrement) {
    LongInteger num("99");
    ++num;
    CHECK(num == LongInteger("100"));
}

TEST(PostIncrement) {
    LongInteger num("99");
    LongInteger old = num++;
    CHECK(old == LongInteger("99"));
    CHECK(num == LongInteger("100"));
}

TEST(PreDecrement) {
    LongInteger num("100");
    --num;
    CHECK(num == LongInteger("99"));
}

TEST(PostDecrement) {
    LongInteger num("100");
    LongInteger old = num--;
    CHECK(old == LongInteger("100"));
    CHECK(num == LongInteger("99"));
}

TEST(OutputStream) {
    CHECK_EQUAL("12345", toString(LongInteger("12345")));
    CHECK_EQUAL("-67890", toString(LongInteger("-67890")));
    CHECK_EQUAL("0", toString(LongInteger("0")));
}

TEST(InputStream) {
    std::istringstream iss1("12345");
    std::istringstream iss2("-67890");
    std::istringstream iss3("0");

    LongInteger a, b, c;
    iss1 >> a; iss2 >> b; iss3 >> c;

    CHECK(a == LongInteger("12345"));
    CHECK(b == LongInteger("-67890"));
    CHECK(c == LongInteger("0"));
}

TEST(InputStreamInvalid) {
    std::istringstream iss("abc");
    LongInteger num;
    iss >> num;
    CHECK(iss.fail());
}

TEST(ZeroOperations) {
    LongInteger zero("0");
    LongInteger one("1");
    LongInteger neg_one("-1");

    CHECK((zero + one) == one);
    CHECK((one - zero) == one);
    CHECK((zero * one) == zero);
    CHECK((zero / one) == zero);
    CHECK((one / one) == one);
    CHECK((one % one) == zero);
}

TEST(LargeNumberComparison) {
    LongInteger a("999999999999999999999999999999");
    LongInteger b("1000000000000000000000000000000");
    CHECK(a < b);
}

TEST(MinusOneMultiplication) {
    LongInteger a("12345678901234567890");
    LongInteger b("-1");
    CHECK(a * b == LongInteger("-12345678901234567890"));
}

TEST(MinusOneDivision) {
    LongInteger a("-98765432109876543210");
    LongInteger b("-1");
    CHECK(a / b == LongInteger("98765432109876543210"));
}

} // SUITE

int main() {
    return UnitTest::RunAllTests();
}