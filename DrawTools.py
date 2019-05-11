import sys

sys.setrecursionlimit(8000)

def flood_fill(TiledMap, pos, tile_id, out_list):
	old_id = TiledMap.map_.grid[pos[0]][pos[1]]

	# Recursion stop
	if(old_id == tile_id):
		return

	out_list.append(pos)

	if(pos[0]>=0 and flood_check(TiledMap, pos, tile_id, out_list, x=-1)):
		sec_flood_fill(TiledMap, [pos[0]-1, pos[1]], tile_id, out_list)
	if(pos[0] < len(TiledMap.map_.grid)-1 and flood_check(TiledMap, pos, tile_id, out_list, x=1)):
		sec_flood_fill(TiledMap, [pos[0]+1, pos[1]], tile_id, out_list)
	if(pos[1]>0 and flood_check(TiledMap, pos, tile_id, out_list, y=-1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]-1], tile_id, out_list)
	if(pos[1] < len(TiledMap.map_.grid[0])-1 and flood_check(TiledMap, pos, tile_id, out_list, y=1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]+1], tile_id, out_list)

	return out_list

def sec_flood_fill(TiledMap, pos, tile_id, out_list):

	out_list.append(pos)

	if(pos[0]>0 and flood_check(TiledMap, pos, tile_id, out_list, x=-1)):
		sec_flood_fill(TiledMap, [pos[0]-1, pos[1]], tile_id, out_list)
	if(pos[0] < len(TiledMap.map_.grid)-1 and flood_check(TiledMap, pos, tile_id, out_list, x=1)):
		sec_flood_fill(TiledMap, [pos[0]+1, pos[1]], tile_id, out_list)
	if(pos[1]>0 and flood_check(TiledMap, pos, tile_id, out_list, y=-1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]-1], tile_id, out_list)
	if(pos[1] < len(TiledMap.map_.grid[0])-1 and flood_check(TiledMap, pos, tile_id, out_list, y=1)):
		sec_flood_fill(TiledMap, [pos[0], pos[1]+1], tile_id, out_list)

def flood_check(TiledMap, pos, tile_id, out_list, x=0, y=0):
	if(TiledMap[pos[0]+x][pos[1]+y] != tile_id and [pos[0]+x, pos[1]+y] not in out_list):
		return True
	return False