// src/long_integer.cpp
#include "long_integer.h"
#include <algorithm>
#include <cctype>
#include <string>
#include <sstream>

LongInteger::LongInteger() : digits_(1, 0), is_negative_(false) {}

LongInteger::LongInteger(const std::string& str) : is_negative_(false) {
  if (str.empty()) {
    throw std::invalid_argument("Empty string");
  }

  size_t start = 0;
  if (str[0] == '-') {
    is_negative_ = true;
    start = 1;
  } else if (str[0] == '+') {
    start = 1;
  }

  if (start >= str.size()) {
    throw std::invalid_argument("Only sign");
  }

  for (size_t i = start; i < str.size(); ++i) {
    if (!std::isdigit(static_cast<unsigned char>(str[i]))) {
      throw std::invalid_argument("Invalid digit");
    }
  }

  size_t first_nonzero = start;
  while (first_nonzero < str.size() && str[first_nonzero] == '0') {
    ++first_nonzero;
  }

  if (first_nonzero == str.size()) {
    digits_ = {0};
    is_negative_ = false;
  } else {
    digits_.clear();
    for (size_t i = str.size(); i > first_nonzero; --i) {
      digits_.push_back(str[i - 1] - '0');
    }
  }
}

LongInteger::LongInteger(const LongInteger& other)
    : digits_(other.digits_), is_negative_(other.is_negative_) {}

LongInteger& LongInteger::operator=(const LongInteger& other) {
  if (this != &other) {
    digits_ = other.digits_;
    is_negative_ = other.is_negative_;
  }
  return *this;
}

void LongInteger::RemoveLeadingZeros() {
  while (digits_.size() > 1 && digits_.back() == 0) {
    digits_.pop_back();
  }
  if (digits_.size() == 1 && digits_[0] == 0) {
    is_negative_ = false;
  }
}

int LongInteger::CompareAbsolute(const LongInteger& other) const {
  if (digits_.size() != other.digits_.size()) {
    return digits_.size() > other.digits_.size() ? 1 : -1;
  }
  for (int i = static_cast<int>(digits_.size()) - 1; i >= 0; --i) {
    if (digits_[i] != other.digits_[i]) {
      return (digits_[i] > other.digits_[i]) ? 1 : -1;
    }
  }
  return 0;
}

LongInteger LongInteger::AddPositive(const LongInteger& other) const {
  LongInteger res;
  res.digits_.clear();
  int carry = 0;
  size_t n = std::max(digits_.size(), other.digits_.size());
  for (size_t i = 0; i < n || carry; ++i) {
    int sum = carry;
    if (i < digits_.size()) sum += digits_[i];
    if (i < other.digits_.size()) sum += other.digits_[i];
    res.digits_.push_back(sum % 10);
    carry = sum / 10;
  }
  return res;
}

LongInteger LongInteger::SubtractPositive(const LongInteger& other) const {
  LongInteger res;
  res.digits_.clear();
  int borrow = 0;
  for (size_t i = 0; i < digits_.size(); ++i) {
    int d = digits_[i] - borrow;
    if (i < other.digits_.size()) d -= other.digits_[i];
    if (d < 0) {
      d += 10;
      borrow = 1;
    } else {
      borrow = 0;
    }
    res.digits_.push_back(d);
  }
  res.RemoveLeadingZeros();
  return res;
}

LongInteger LongInteger::MultiplyPositive(const LongInteger& other) const {
  LongInteger res;
  res.digits_.assign(digits_.size() + other.digits_.size(), 0);
  for (size_t i = 0; i < digits_.size(); ++i) {
    int carry = 0;
    for (size_t j = 0; j < other.digits_.size() || carry; ++j) {
      long long cur = res.digits_[i + j] + carry;
      if (j < other.digits_.size()) {
        cur += static_cast<long long>(digits_[i]) * other.digits_[j];
      }
      res.digits_[i + j] = static_cast<int>(cur % 10);
      carry = static_cast<int>(cur / 10);
    }
  }
  res.RemoveLeadingZeros();
  return res;
}

LongInteger LongInteger::DividePositive(const LongInteger& other) const {
  LongInteger quotient;
  LongInteger remainder;
  for (int i = static_cast<int>(digits_.size()) - 1; i >= 0; --i) {
    remainder.digits_.insert(remainder.digits_.begin(), digits_[i]);
    remainder.RemoveLeadingZeros();
    int digit = 0;
    while (remainder.CompareAbsolute(other) >= 0) {
      remainder = remainder.SubtractPositive(other);
      digit++;
    }
    quotient.digits_.insert(quotient.digits_.begin(), digit);
  }
  quotient.RemoveLeadingZeros();
  return quotient;
}

LongInteger LongInteger::ModuloPositive(const LongInteger& other) const {
  LongInteger q = DividePositive(other);
  LongInteger product = q.MultiplyPositive(other);
  LongInteger r = SubtractPositive(product);
  return r;
}

LongInteger LongInteger::operator+(const LongInteger& other) const {
  if (is_negative_ == other.is_negative_) {
    LongInteger res = AddPositive(other);
    res.is_negative_ = is_negative_;
    return res;
  } else {
    int cmp = CompareAbsolute(other);
    if (cmp > 0) {
      LongInteger res = SubtractPositive(other);
      res.is_negative_ = is_negative_;
      return res;
    } else if (cmp < 0) {
      LongInteger res = other.SubtractPositive(*this);
      res.is_negative_ = other.is_negative_;
      return res;
    } else {
      return LongInteger("0");
    }
  }
}

LongInteger& LongInteger::operator+=(const LongInteger& other) {
  *this = *this + other;
  return *this;
}

LongInteger LongInteger::operator-(const LongInteger& other) const {
  LongInteger neg_other = other;
  neg_other.is_negative_ = !neg_other.is_negative_;
  return *this + neg_other;
}

LongInteger& LongInteger::operator-=(const LongInteger& other) {
  *this = *this - other;
  return *this;
}

LongInteger LongInteger::operator*(const LongInteger& other) const {
  if (*this == LongInteger("0") || other == LongInteger("0")) {
    return LongInteger("0");
  }
  LongInteger res = MultiplyPositive(other);
  res.is_negative_ = (is_negative_ != other.is_negative_);
  return res;
}

LongInteger& LongInteger::operator*=(const LongInteger& other) {
  *this = *this * other;
  return *this;
}

LongInteger LongInteger::operator/(const LongInteger& other) const {
  if (other == LongInteger("0")) {
    throw std::domain_error("Division by zero");
  }
  if (*this == LongInteger("0")) {
    return LongInteger("0");
  }
  LongInteger res = DividePositive(other);
  res.is_negative_ = (is_negative_ != other.is_negative_);
  return res;
}

LongInteger& LongInteger::operator/=(const LongInteger& other) {
  *this = *this / other;
  return *this;
}

LongInteger LongInteger::operator%(const LongInteger& other) const {
  if (other == LongInteger("0")) {
    throw std::domain_error("Modulo by zero");
  }
  if (*this == LongInteger("0")) {
    return LongInteger("0");
  }
  LongInteger r = ModuloPositive(other);
  r.is_negative_ = is_negative_;
  return r;
}

LongInteger& LongInteger::operator%=(const LongInteger& other) {
  *this = *this % other;
  return *this;
}

LongInteger& LongInteger::operator++() {
  *this += LongInteger("1");
  return *this;
}

LongInteger LongInteger::operator++(int) {
  LongInteger tmp(*this);
  ++(*this);
  return tmp;
}

LongInteger& LongInteger::operator--() {
  *this -= LongInteger("1");
  return *this;
}

LongInteger LongInteger::operator--(int) {
  LongInteger tmp(*this);
  --(*this);
  return tmp;
}

bool LongInteger::operator==(const LongInteger& other) const {
  return is_negative_ == other.is_negative_ && digits_ == other.digits_;
}

bool LongInteger::operator!=(const LongInteger& other) const {
  return !(*this == other);
}

bool LongInteger::operator>(const LongInteger& other) const {
  if (is_negative_ != other.is_negative_) {
    return !is_negative_;
  }
  if (is_negative_) {
    return CompareAbsolute(other) < 0;
  }
  return CompareAbsolute(other) > 0;
}

bool LongInteger::operator<(const LongInteger& other) const {
  return other > *this;
}

bool LongInteger::operator>=(const LongInteger& other) const {
  return !(*this < other);
}

bool LongInteger::operator<=(const LongInteger& other) const {
  return !(*this > other);
}

std::istream& operator>>(std::istream& is, LongInteger& num) {
  std::string s;
  if (is >> s) {
    try {
      num = LongInteger(s);
    } catch (...) {
      is.setstate(std::ios::failbit);
    }
  }
  return is;
}

std::ostream& operator<<(std::ostream& os, const LongInteger& num) {
  if (num.is_negative_) {
    os << '-';
  }
  for (int i = static_cast<int>(num.digits_.size()) - 1; i >= 0; --i) {
    os << num.digits_[i];
  }
  return os;
}