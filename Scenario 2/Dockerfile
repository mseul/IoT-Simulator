FROM alpine

#Note: If running this on a Raspberry Pi with Docker, this needs a manual libseccomp update
#If not applied, signature checks will fail when calling apk
#https://docs.linuxserver.io/faq#libseccomp
#The default library has an issue that prevents the docker images from accessing the proper time
#Call "docker run -it alpine /bin/date" and if it returns 1970 as current date, apply libseccomp update
#ssh setup steps adapted from Oscar Andrés Díaz (https://github.com/oadiazm/alpine-ssh/blob/master/Dockerfile)

#Also, this configuration is not secured, with the keys giving full root access to the system.
#A proper way would be to create a separate, restricted user for either access and assign keys for those, disabling root logins entirely.
#Furthermore, instead of using a generic peering key across the container pop, each container should receive a distinct key.
#These shortcuts were taken to demonstrate that the blind peer replay of commands is generally viable.

RUN apk --update add --no-cache openssh bash \
  && sed -i s/#PermitRootLogin.*/PermitRootLogin\ yes/ /etc/ssh/sshd_config \
  && echo "root:fekjhe5vdfpobqewlpxyujklxcdrjpfbw" | chpasswd \
  && rm -rf /var/cache/apk/* \
  && sed -ie 's/#Port 22/Port 22/g' /etc/ssh/sshd_config \
  && sed -ri 's/#HostKey \/etc\/ssh\/ssh_host_key/HostKey \/etc\/ssh\/ssh_host_key/g' /etc/ssh/sshd_config \
  && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_rsa_key/HostKey \/etc\/ssh\/ssh_host_rsa_key/g' /etc/ssh/sshd_config \
  && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_dsa_key/HostKey \/etc\/ssh\/ssh_host_dsa_key/g' /etc/ssh/sshd_config \
  && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ecdsa_key/HostKey \/etc\/ssh\/ssh_host_ecdsa_key/g' /etc/ssh/sshd_config \
  && sed -ir 's/#HostKey \/etc\/ssh\/ssh_host_ed25519_key/HostKey \/etc\/ssh\/ssh_host_ed25519_key/g' /etc/ssh/sshd_config \
  && /usr/bin/ssh-keygen -A \
  && ssh-keygen -t rsa -b 4096 -f  /etc/ssh/ssh_host_key
RUN mkdir -p /root/.ssh
ADD compliance_server_shared.pub /root/compliance_server_shared.pub
ADD peering_key.pub /root/peering_key.pub
ADD peering_key /root/peering_key
ADD audit_replay.sh /root/audit_replay.sh
RUN cat /root/compliance_server_shared.pub >> /root/.ssh/authorized_keys
RUN cat /root/peering_key.pub >> /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN chmod 600 /root/peering_key
RUN chmod 744 /root/audit_replay.sh
EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]
