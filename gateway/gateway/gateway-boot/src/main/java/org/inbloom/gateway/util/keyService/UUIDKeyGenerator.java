package org.inbloom.gateway.util.keyService;

import org.apache.commons.codec.binary.Base64;
import org.springframework.stereotype.Service;

import java.nio.ByteBuffer;
import java.util.UUID;

/**
 *
 */
@Service
public class UUIDKeyGenerator implements KeyGenerator {

    public String generateKey()
    {
        UUID uuid = UUID.randomUUID();

        ByteBuffer bb = ByteBuffer.wrap(new byte[16]);
        bb.putLong(uuid.getMostSignificantBits());
        bb.putLong(uuid.getLeastSignificantBits());
        byte[] byteArray =  bb.array();

        //make url-safe encodings
        Base64 base64 = new Base64(true);

        return new String(base64.encode(byteArray));
    }

}
