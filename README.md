# EksiPol
Political Polarization works on EksiSozluk.com. It includes two different type of scrapers and also a network modeling algorithm prepared for social phenomena.



https://github.com/user-attachments/assets/79149652-202b-4033-9ecd-650b7e8da6a5



https://github.com/user-attachments/assets/ae93db13-40b7-4d4b-bf38-be49797bb4e0



# Polarized Network Generator



### 3 Polarized 1 Non Polarized Topic, Alignment 0.03, Homophily: Strong (Controversal Topic and Non Controversal Topic)

```
EXAMPLE = generate_aligned_user_space_mixed(100,1,3,0,0.03)
POL = SEQ_GENERATOR(EXAMPLE)
POL.calculate_similarity(method= 'euc')
POL.accept_deg_dist(np.random.randint(low = 1, high = 10, size = POL.user_space.shape[0]))
graph = POL.connect_sequential(HPOW= 100)
POL.PLOT(1)
ig.plot(POL.network, vertex_color = POL.network.vs["color"])
```
![Ekran Resmi 2024-10-13 17 04 59](https://github.com/user-attachments/assets/9decf964-1632-4c37-87a3-492a5fa87bb2)


```
POL.PLOT(0)
ig.plot(POL.network, vertex_color = POL.network.vs["color"])
```
![Ekran Resmi 2024-10-13 17 05 26](https://github.com/user-attachments/assets/f0e73d4f-880c-4388-aacf-59052050024f)



### 3 Polarized 1 Non Polarized Topic, Alignment 0.03, Homophily: Extremely Low (Controversal Topic)

```
EXAMPLE = generate_aligned_user_space_mixed(100,1,3,0,0.03)
POL = SEQ_GENERATOR(EXAMPLE)
POL.calculate_similarity(method= 'euc')
POL.accept_deg_dist(np.random.randint(low = 1, high = 10, size = POL.user_space.shape[0]))
graph = POL.connect_sequential(HPOW= 0.3)
POL.PLOT(1)
print('Network Generated with 3 Polarized and 1 Non Polarized Topic with Alignment Parameter 0.03 and Homophily Parameter 0.3')
ig.plot(POL.network, vertex_color = POL.network.vs["color"])
```
![Ekran Resmi 2024-10-13 17 06 02](https://github.com/user-attachments/assets/6c876c55-0fa5-4f34-bc29-ee233834e00d)


### 3 Polarized 1 Non Polarized Topic, Alignment 0.03, Homophily: Extremely Strong (Controversal Topic)
```
EXAMPLE = generate_aligned_user_space_mixed(100,1,20,0,0.01)
POL = SEQ_GENERATOR(EXAMPLE)
POL.calculate_similarity(method= 'euc')
POL.accept_deg_dist(np.random.randint(low = 1, high = 15, size = POL.user_space.shape[0]))
graph = POL.connect_sequential(HPOW= 3000)
POL.PLOT(1)
ig.plot(POL.network, vertex_color = POL.network.vs["color"])
```
![Ekran Resmi 2024-10-13 17 06 32](https://github.com/user-attachments/assets/1135dda8-3a14-4e5d-aea3-b584d69dac06)

Generating Extremely Polarized Societies is also possible. In this case, the nodes prefer not to connect.

![IMAGE 2024-10-13 16_49_15](https://github.com/user-attachments/assets/ad4082d7-e204-43ac-8cc8-07a851242cd8)








