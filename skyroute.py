from graph_search import bfs, dfs
from vc_metro import vc_metro
from vc_landmarks import vc_landmarks
from landmark_choices import landmark_choices

# Build your program below:
#define a variable that is a string that joins all the landmarks together
landmark_string=""
for landmark in landmark_choices:
  landmark_string+=str(landmark)+" "+str(landmark_choices[landmark]) +"\n"

#help to account for stations closings
stations_under_construction=['Waterfront']

def get_active_stations():
  updated_metro=vc_metro
  for station in stations_under_construction:
    for current_station, neighboring_stations in updated_metro.items():
      if current_station not in stations_under_construction:
        updated_metro[current_station]-=set(stations_under_construction)
      else:
        updated_metro[current_station]=set([])
  return updated_metro    

#define greet function that prints two statements
def greet():
  print("Hi there and welcome to SkyRoute! \n")
  print("""We'll help you find the shortest route between the following Vancouver landmarks:\n""" + landmark_string)

#define goodbye function for the end of the porgram
def goodbye():
  print("Thanks for using SkyRoute!")

#define skyroute function which is the main function of this program
def skyroute():
  greet()
  new_route()
  goodbye()
  
#define set_start_and_end function
def set_start_and_end(start_point,end_point):
  if start_point is not None:
    change_point=input("What would you like to change? You can enter 'o' for 'origin', 'd' for 'destination', or 'b' for 'both':")
    if change_point=="b":
      start_point=get_start()
      end_point=get_end()
    elif change_point=="o":
      start_point=get_start()
    elif change_point=="d":
      end_point=get_end()
    else:
      print("Oops, that isn't 'o', 'd', or 'b'...")
      set_start_and_end(start_point,end_point)
  else:
    start_point=get_start()
    end_point=get_end()
  return start_point,end_point

#define get_start function that gets an orgin from user
def get_start():
  start_point_letter=input("Where are you coming from? Type in the corresponding letter:")
  if start_point_letter in landmark_choices:
    start_point=landmark_choices[start_point_letter]
    return start_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    get_start()

#define get end which will request a destination from the user
def get_end():
  end_point_letter=input("Where are you headed? Type in the corresponding letter:")
  if end_point_letter in landmark_choices:
    end_point=landmark_choices[end_point_letter]
    return end_point
  else:
    print("Sorry, that's not a landmark we have data on. Let's try this again...")
    get_end()

#define new route function that gets origin and destination, search for best route, allow users to search for another route
def new_route(start_point=None,end_point=None):
  start_point, end_point =set_start_and_end(start_point,end_point)
  shortest_route=get_route(start_point,end_point)
  if shortest_route:
    shortest_route_string='\n'.join(shortest_route)
    print("The shortest metro route from {0} to {1} is:\n{2}".format(start_point, end_point, shortest_route_string))
  else:
    print("Unfortunately, there is currently no path between {0} and {1} due to maintenance.".format(start_point, end_point))
  again=input("Would you like to see another route? Enter y/n: ")
  if again=="y":
    show_landmarks()
    new_route(start_point,end_point)

#define show landmarks function which asks if they want to see the landmarks
def show_landmarks():
  see_landmarks=input("Would you like to see the list of landmarks again? Enter y/n: ")
  if see_landmarks=="y":
    print(landmark_string)



#define get route function that finds the best route
def get_route(start_point,end_point):
  #each landmark could have several start stations and several end stations
  start_stations=vc_landmarks[start_point]
  end_stations=vc_landmarks[end_point]
  routes=[]
  #for each start station, and for each end station, see if there is a route
  for sstation in start_stations:
    for estation in end_stations:
      metro_system=get_active_stations() if stations_under_construction else vc_metro      
      if stations_under_construction !=[]:
        possible_route=dfs(metro_system, sstation,estation)
        if not possible_route:
          return None
      route=bfs(metro_system,sstation,estation)

      #if the route exists, add to list
      if route:
        routes.append(route)
      
  #find the shortest route
  shortest_route=min(routes, key=len)
  return shortest_route
  
skyroute()