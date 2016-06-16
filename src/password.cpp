#include "password.hpp"

#include <boost/uuid/sha1.hpp>
#include <boost/archive/iterators/base64_from_binary.hpp>
#include <boost/archive/iterators/transform_width.hpp>
#include <boost/algorithm/string.hpp>

std::string encode64(const std::string& val) {
    using namespace boost::archive::iterators;
    using It = base64_from_binary<transform_width<std::string::const_iterator, 6, 8>>;
    auto tmp = std::string(It(std::begin(val)), It(std::end(val)));
    return tmp.append((3 - val.size() % 3) % 3, '=');
}

std::string calculatePassword(const std::string& secret, const std::string& alias) {
	std::string secretAndAlias = secret + alias;
	boost::uuids::detail::sha1 sha1;
	sha1.process_bytes(secretAndAlias.c_str(), secretAndAlias.size());
	unsigned int digest[5];
	sha1.get_digest(digest);
	std::string hash;
	hash.resize(20);
	for (size_t i = 0; i < 5; ++i) {
		// Swap byte order because of Little Endian
		const char* tmp = reinterpret_cast<char*>(digest);
		hash[i * 4    ] = tmp[i * 4 + 3];
		hash[i * 4 + 1] = tmp[i * 4 + 2];
		hash[i * 4 + 2] = tmp[i * 4 + 1];
		hash[i * 4 + 3] = tmp[i * 4    ];
	}
	return encode64(hash).substr(0, 16);
}
