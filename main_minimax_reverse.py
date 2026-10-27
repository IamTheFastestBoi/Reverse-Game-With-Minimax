import pygame
import sys
import random
import copy
# oyunun pygame arayuzu yapay zeka ile yapildi .

class OyunMotoru:
    def __init__(self , oyunTahtasi , oyuncuPC , oyuncuInsan):
        self.oyuncuPC = oyuncuPC
        self.oyuncuInsan = oyuncuInsan
        self.oyunTahtasi = oyunTahtasi
        self.hakem = Hakem(self.oyunTahtasi)
        self.zeka = MINIMAX_ZEKA(self.oyunTahtasi.oyunTahtasi, self.oyuncuPC)
        pygame.init()
        self.KARE_BOYUTU = 80 
        self.GENISLIK = self.KARE_BOYUTU * 8
        self.YUKSEKLIK = self.KARE_BOYUTU * 8
        self.ekran = pygame.display.set_mode((self.GENISLIK, self.YUKSEKLIK))
        pygame.display.set_caption("Serbest Yerleşim Reversi")
        self.RENK_ZEMIN = (34, 139, 34) 
        self.RENK_CIZGI = (0, 0, 0)     
        self.RENK_INSAN = (0, 0, 0)     
        self.RENK_PC = (255, 255, 255)
    def draw_board(self):
        self.ekran.fill(self.RENK_ZEMIN) 
        
    
        for i in range(9):
            pygame.draw.line(self.ekran, self.RENK_CIZGI, (0, i * self.KARE_BOYUTU), (self.GENISLIK, i * self.KARE_BOYUTU), 2)
            pygame.draw.line(self.ekran, self.RENK_CIZGI, (i * self.KARE_BOYUTU, 0), (i * self.KARE_BOYUTU, self.YUKSEKLIK), 2)
            
        
        for i in range(8):
            for j in range(8):
                kare_degeri = self.oyunTahtasi.oyunTahtasi[i][j]
                
                merkez_x = j * self.KARE_BOYUTU + self.KARE_BOYUTU // 2
                merkez_y = i * self.KARE_BOYUTU + self.KARE_BOYUTU // 2
                yaricap = self.KARE_BOYUTU // 2 - 5
                
                if kare_degeri == 1:
                    pygame.draw.circle(self.ekran, self.RENK_INSAN, (merkez_x, merkez_y), yaricap)
                elif kare_degeri == -1:
                    pygame.draw.circle(self.ekran, self.RENK_PC, (merkez_x, merkez_y), yaricap)
        pygame.display.flip() 
    def hamleYap_Oyuncu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    fare_x, fare_y = event.pos
                    self.Oyuncu_inputHamle_y = fare_x // self.KARE_BOYUTU
                    self.Oyuncu_inputHamle_x = fare_y // self.KARE_BOYUTU
                    
                    if 0 <= self.Oyuncu_inputHamle_x < 8 and 0 <= self.Oyuncu_inputHamle_y < 8:
                        return (self.Oyuncu_inputHamle_x, self.Oyuncu_inputHamle_y)

    def hamleYap_PC(self , x, y):
        self.PC_inputHamle_x = x
        self.PC_inputHamle_y = y
        return (self.PC_inputHamle_x , self.PC_inputHamle_y)
    def hamleKontrol_Oyuncu(self):
        if self.oyunTahtasi.oyunTahtasi[self.Oyuncu_inputHamle_x][self.Oyuncu_inputHamle_y] == 0:
            return True
        else:
            return False
    def hamleKontrol_PC(self):
        if self.oyunTahtasi.oyunTahtasi[self.PC_inputHamle_x][self.PC_inputHamle_y] == 0:
            return True
        else:
            return False    
    def oyunmotoru(self):
        while True:
            self.draw_board()
            while True:
                self.hamleYap_Oyuncu()
                if self.hamleKontrol_Oyuncu() == True:
                    self.oyunTahtasi.oyunTahtasi[self.Oyuncu_inputHamle_x][self.Oyuncu_inputHamle_y] = 1
                    self.hakem.reverse(self.Oyuncu_inputHamle_x , self.Oyuncu_inputHamle_y , 1) 
                    break
                else:
                    print("Geçersiz hamle! Lütfen tekrar deneyin.")
                    continue
            self.draw_board()
            print("PC dusunuyor...")
            virtual_copy = copy.deepcopy(self.oyunTahtasi.oyunTahtasi)
            _ , (pc_hedef_x, pc_hedef_y) = self.zeka.virtual_moves(virtual_copy, self.oyuncuPC, depth=4, alpha=-9999, beta=9999)
            if pc_hedef_x is not None and pc_hedef_y is not None:
                self.hamleYap_PC(pc_hedef_x, pc_hedef_y)
                if self.hamleKontrol_PC() == True:
                    print(f"PC hamlesi: ({self.PC_inputHamle_x}, {self.PC_inputHamle_y})")
                    self.oyunTahtasi.oyunTahtasi[self.PC_inputHamle_x][self.PC_inputHamle_y] = -1
                    self.hakem.reverse(self.PC_inputHamle_x, self.PC_inputHamle_y, -1)
            else:
                print("PC için geçerli bir hamle bulunamadı.")
                break
            bos_var, insan_skor, pc_skor = self.oyunTahtasi.skor_ve_bitis_kontrol()
            if not bos_var:
                print(f"\nOyun Bitti! Tahta tamamen doldu.")
                print(f"Senin Skorun (X): {insan_skor}")
                print(f"Bilgisayarın Skoru (O): {pc_skor}")
                if insan_skor > pc_skor:
                    print("Tebrikler, Kazandın! 🏆")
                elif pc_skor > insan_skor:
                    print("Bilgisayar Kazandı! 🤖")
                else:
                    print("Oyun Berabere! 🤝")
                break


class Hakem:    
    def __init__(self , oyunTahtasi):
        self.oyunTahtasi = oyunTahtasi
        self.vectors = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
        self.oyuncu = 1
        self.pc = -1
    def reverse(self , x , y , currentPlayer):
        otherPlayer = currentPlayer * -1
        for dx , dy in self.vectors:
            temporaryList = []
            vectorX = x + dx
            vectorY = y + dy
            while 0 <= vectorX < 8 and 0 <= vectorY < 8:
                checked_value = self.oyunTahtasi.oyunTahtasi[vectorX][vectorY]
                if checked_value == otherPlayer:
                    temporaryList.append((vectorX , vectorY))
                    vectorX += dx
                    vectorY += dy
                elif checked_value == currentPlayer:
                    if len(temporaryList) > 0:
                        for reverseX , reverseY in temporaryList:
                            self.oyunTahtasi.oyunTahtasi[reverseX][reverseY] = currentPlayer
                    break
                else:
                    break


class MINIMAX_ZEKA:
    def __init__(self , oyunTahtasi , pc_renk):
        self.oyunTahtasi = oyunTahtasi
        self.sanal_board = self.oyunTahtasi
        self.pc_renk = pc_renk
        self.oyuncu = pc_renk * -1
        self.puan_haritasi = [
            [ 100, -20,  10,   5,   5,  10, -20,  100],
            [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
            [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
            [   5,  -2,  -1,  -1,  -1,  -1,  -2,    5],
            [   5,  -2,  -1,  -1,  -1,  -1,  -2,    5],
            [  10,  -2,  -1,  -1,  -1,  -1,  -2,   10],
            [ -20, -50,  -2,  -2,  -2,  -2, -50, -20],
            [ 100, -20,  10,   5,   5,  10, -20, 100]
        ]
        self.oyuncu = 1
        self.pc = -1
        self.vectors = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    def undo_move(self, current_board, x , y , other_player , changed_pieces):
        current_board[x][y] = 0
        if len(changed_pieces) > 0:
            for reverseX , reverseY in changed_pieces:
                current_board[reverseX][reverseY] = other_player

    def sanal_reverse(self , x , y , currentPlayer  , sanal_tahta):
        otherPlayer = currentPlayer * -1
        changed_pieces = []
        for dx , dy in self.vectors:
            temporaryList = []
            vectorX = x + dx
            vectorY = y + dy
            while 0 <= vectorX < 8 and 0 <= vectorY < 8:
                checked_value = sanal_tahta[vectorX][vectorY]
                if checked_value == otherPlayer:
                    temporaryList.append((vectorX , vectorY))
                    vectorX += dx
                    vectorY += dy
                elif checked_value == currentPlayer:
                    if len(temporaryList) > 0:
                        for reverseX , reverseY in temporaryList:
                            sanal_tahta[reverseX][reverseY] = currentPlayer
                            changed_pieces.append((reverseX, reverseY))
                    break
                else:
                    break
        return changed_pieces
 
    def virtual_moves(self , current_board  , current_player , depth = 4 , alpha = -9999 , beta = 9999):
        if depth == 0:
            return self.calculate_the_board_score(current_board) , None
        if current_player == self.pc_renk:
            best_score = -9999 
        else:
            best_score = 9999
        prunned = False
        best_moves_list = []
        is_move_possible = False
        for i in range(8):
            if prunned:
                break
            for j in range(8):
                if current_board[i][j] == 0:
                    is_move_possible = True
                    current_board[i][j] = current_player
                    changed_pieces = self.sanal_reverse(i , j , current_player , current_board)
                    expected_score , _ = self.virtual_moves(current_board , current_player * -1 , depth - 1 , alpha , beta)
                    self.undo_move(current_board  , i , j , current_player * -1 , changed_pieces)
                    if current_player == self.pc_renk:
                        if expected_score > best_score:
                            best_score = expected_score
                            best_moves_list = [(i, j)]
                        elif expected_score == best_score:
                            best_moves_list.append((i, j))
                        alpha = max(alpha, best_score)
                        if alpha >= beta:
                            prunned = True
                            break
                    if current_player == self.oyuncu:
                        if expected_score < best_score:
                            best_score = expected_score
                            best_moves_list = [(i, j)]
                        elif expected_score == best_score:
                            best_moves_list.append((i, j))
                        beta = min(beta, best_score)
                        if alpha >= beta:
                            prunned = True
                            break
        if not is_move_possible:
            return self.calculate_the_board_score(current_board) , None
        return best_score , random.choice(best_moves_list)
    def calculate_the_board_score(self , current_board):

        sanal_harita = [row[:] for row in self.puan_haritasi]
        
        if current_board[0][0] == self.pc_renk:
            sanal_harita[0][1] = 20
            sanal_harita[1][0] = 20
            sanal_harita[1][1] = 30 

        if current_board[0][7] == self.pc_renk:
            sanal_harita[0][6] = 20
            sanal_harita[1][7] = 20
            sanal_harita[1][6] = 30

        if current_board[7][0] == self.pc_renk:
            sanal_harita[6][0] = 20
            sanal_harita[7][1] = 20
            sanal_harita[6][1] = 30 

        if current_board[7][7] == self.pc_renk:
            sanal_harita[7][6] = 20
            sanal_harita[6][7] = 20
            sanal_harita[6][6] = 30
        toplam_harita_puani = 0
        pc_tas_sayisi = 0
        oyuncu_tas_sayisi = 0

        for i in range(8):
            for j in range(8):
                if current_board[i][j] == self.pc_renk:
                    toplam_harita_puani += sanal_harita[i][j]
                    pc_tas_sayisi += 1
                elif current_board[i][j] == self.oyuncu:
                    toplam_harita_puani -= sanal_harita[i][j]
                    oyuncu_tas_sayisi += 1
                    
        tas_ustunlugu_puani = (pc_tas_sayisi - oyuncu_tas_sayisi) * 10
        
        return toplam_harita_puani + tas_ustunlugu_puani


class OyunTahtasi:
    def __init__(self):
        self.oyunTahtasi = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]
    def initialize_board(self):
        print("\n 0 1 2 3 4 5 6 7")
        for i in range(8):
            row = str(i) + " "
            for j in range(8):
                if self.oyunTahtasi[i][j] == 1:
                    row += "X "
                elif self.oyunTahtasi[i][j] == -1:
                    row += "O "
                else:
                    row += ". "
            print(row)
        print("-" * 20)
    def skor_ve_bitis_kontrol(self):
        bos_yer_var = False
        insan_puan = 0
        pc_puan = 0
        
        for i in range(8):
            for j in range(8):
                if self.oyunTahtasi[i][j] == 0:
                    bos_yer_var = True
                elif self.oyunTahtasi[i][j] == 1:
                    insan_puan += 1
                elif self.oyunTahtasi[i][j] == -1:
                    pc_puan += 1
                    
        return bos_yer_var, insan_puan, pc_puan


if __name__ == "__main__":
    tahta = OyunTahtasi()
    motor = OyunMotoru(tahta, oyuncuPC=-1, oyuncuInsan=1)
    print("Oyun Başladı!")
    motor.oyunmotoru()