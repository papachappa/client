#!/bin/bash
# doc: http://serverfault.com/questions/340887/using-a-self-signed-ssl-cert-for-an-https-based-internal-apt-repository

SERVER="tpapt.lokc-media.dynamic-dns.net"
APTHTTPSUSER=aptuser
APTHTTPSPASS=2NdGAWXbT3
KEYFILE=loewe_tpapt2017.gpg.key

APTCONFFILE=/etc/apt/sources.list.d/loewe_tpapt.list
echo "Adding repository to apt configuration (file: ${APTCONFFILE})"
echo -e "deb https://${APTHTTPSUSER}:${APTHTTPSPASS}@${SERVER}/ubuntu $(grep DISTRIB_CODENAME /etc/lsb-release | cut -d '=' -f2) main" |  tee ${APTCONFFILE}

APTCONFFILE=/etc/apt/apt.conf.d/99loewe_ssl
echo "Adding SSL certification exception to apt configuration (file: ${APTCONFFILE})"
echo -e "Acquire::https::${SERVER}::Verify-Peer \"false\";" |  tee ${APTCONFFILE}
echo -e "Acquire::https::${SERVER}::Verify-Host \"false\";" |  tee -a ${APTCONFFILE}

echo "Downloading APT repository public key from ${SERVER}"
curl -k "https://${APTHTTPSUSER}:${APTHTTPSPASS}@${SERVER}/ubuntu/${KEYFILE}" |  apt-key add -
if [ $? -ne 0 ]; then
KEYFILE=/tmp/loewe_tpapt2017.key
#-------------------- APT - KEY                            --------------------#
cat <<'EOF' >> ${KEYFILE}
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: GnuPG v1

mQENBFikRxsBCADh4Gagmg0hkoCg7HBOQLotHAEWAug8ZlQooUH4TSfzobX1ozHy
Qv6YjQMGJSYKnF49g7Cvd8cpJBQ8YMekX/Y/PSd8QwO+Is7h57h5XOvXUmuFOR/4
Sum1pu3wCL/R9fMB4lvQrnFUDjmKEER09HdK4A5eU1RZYvuBQrlLLylsFESVD3jV
yidY6N6pWhQkvtOaTo7amHMx2tXr6QfA7BaWbqFGqqgWyJ8Mnrf8pBbui6M8fyfs
eCch4OluiyHoqy1aqIdhOjlp7xn8MjEFnfCnHta1rIxUri/ZhH2AcX9DefQoiNT0
wPsWRPYqJQzjJZFA0sj554ifPlL4t5tqNIVBABEBAAG0a0xPRVdFLiBUZXN0cG9y
dGFsIEFwdC1SZXBvc2l0b3J5ICgyMDE3KSAoTE9FV0UuIGFwdCByZXBvc2l0b3J5
IGtleSAvIGNlcnQgZm9yIHRlc3Rwb3J0YWxzKSA8SVQuVEtAbG9ld2UuZGU+iQE4
BBMBAgAiBQJYpEcbAhsDBgsJCAcDAgYVCAIJCgsEFgIDAQIeAQIXgAAKCRDi482N
9t79LAY5CAC0d4hK+gws5tDtLuJyYlbl8bk7RFMxpCcrWXKeM7nrbjamto1utlVE
HNrnC7yMXOSAf2osTlAz6WibyxhgrWbqO+g0hDE+eOuApb5k4p6WJyvWSNxdt94D
iycqHqSvk3Pq8ptbzXbeSymgOJzQWdVAerzb0FoJ1Eyuh320zefPc81NLDQtnoNu
vSuHP9FyNC49V+bnXwvvxuEaAqUetoCgQ2N2Ek0mQU6ZdEEubmY9VkoqDvZKL15e
rZMVCs9ApfT5PaIciOqtbf9hpAScrl18v9b1P1O5hByMaFRphXP3+Ups+FnVrIgi
T4bwDwx5HvJgLAQ9fl/KeR24RuQFLskruQENBFikRxsBCADkNN/oJT5J+l71nnbf
Ed/9qoWRAoNF66ip6hUdTaAn8+pOAfJa2tkNCiU3PtYLwCqzr830rq++WkZVrT6y
4iU1R1v/hHp3iajyc0RbrWaXJKLHfp/BASPsl2wnEmbpKt5vxd9aczrIvTHqDc3K
dIX4IXDd8mAwbmh3Jh2b8N+LSJ2nWnHyzj/OUeuCemSp54DT1jacu1eietItdhQO
oFCiLtsI/Fqc76Hg81bV6O9SDlXgs8atV4bMv/fff9TLR4ZCg9XTaC7rKpDFP+CW
55Py6g6eyEnq+/BYzMxjKlTvdQ0GZMxHkZ+JysqvN7v8BWHpkcVUBShSsyfkV8z6
CtGdABEBAAGJAR8EGAECAAkFAlikRxsCGwwACgkQ4uPNjfbe/SzZgAgAgqZAQoZf
ACzm5+J2uQN3q7b/YH9o6LA1AXrOY3/1QUTLjeswYMsdTBQioSBrgjaph/E+XzHE
0Ig0RIgB3Br0ugqxvwUtOj2X9GLuAH3YuLeLvDVFWtxczQFPYysoxtDClkoE9pRY
4bFhTxCKE1afwRLan5U4Vy/Z+M2I56D0FrvLD2s3/zt9laIK8q7p5jdCqaTrdXVe
CII/hn+7we7rFQcbo38WRPUU5JSY+fXm5aeup9jpF1Ck7uBh0iCEPlsUtusLZpfF
t3T4+kQJZ3AAlu3JjmvBdMHXQ+o7d+4lbjOwRs8v8//+B2HpXQLLum7kUelYRLtC
DioNuG29zb8b5Q==
=Lb/Y
-----END PGP PUBLIC KEY BLOCK-----
EOF
	 apt-key add ${KEYFILE}
fi
exit 0
