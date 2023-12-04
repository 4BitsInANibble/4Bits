import { StatusBar } from 'expo-status-bar';
import { SafeAreaView, ScrollView, StyleSheet, Text, View } from 'react-native';
import React, { Component } from 'react';
import { Appbar, BottomNavigation, FAB, useTheme, Searchbar, Button } from 'react-native-paper';
import {SafeAreaProvider} from 'react-native-safe-area-context';


const BOTTOM_APPBAR_HEIGHT = 80;
const MEDIUM_FAB_HEIGHT = 56;

const App = () => {

  const [searchQuery, setSearchQuery] = React.useState('');
  const onChangeSearch = query => setSearchQuery(query);

  const theme = useTheme();
  // return(
    
  //   <Searchbar placeholder="Search"
  //   onChangeText={onChangeSearch}
  //   value={searchQuery}
  //   />
  // );

  return (

    <SafeAreaProvider>
    <SafeAreaView>
      <Text style={styles.head} variant="displayMedium">What would you like to cook today?</Text>
      <Searchbar style={styles.search} lightTheme placeholder="Search" onChangeText={onChangeSearch} value={searchQuery} elevation="2"/>
      <Button style={styles.button} mode="contained-tonal" textColor="#faf0e6" buttonColor="#ffb347" onPress={() => {}}>Explore your pantry</Button>
      <Button style={styles.button} mode="contained-tonal" textColor="#faf0e6" buttonColor="#ffb347" onPress={() => {}}>Check your shopping cart</Button>
        <Appbar style={styles.item} >  
        <Appbar.Action size= {30} color= 'orange' icon="home" onPress={() => {}} />
        <Appbar.Action size= {30} color= 'orange' icon="scan-helper" onPress={() => {}} /> 
        <Appbar.Action size= {30} color= 'orange' icon="fridge-bottom" onPress={() => {}} />
        <Appbar.Action size= {30} color= 'orange' icon="cart-heart" onPress={() => {}} />
        <Appbar.Action size= {30} color= 'orange' icon="account" onPress={() => {}} /> 
        </Appbar> 

    </SafeAreaView>
    </SafeAreaProvider>


  );
    
};




const styles = StyleSheet.create({
  head: {
    marginTop: 170,
    textAlign: 'center',
    fontSize: 35,
    fontWeight: '500',
    margin: 50,
  },

  item: {
    marginTop: 245,
    display: 'flex',
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'black'
  },
  search: {
    marginTop: -30,
    position: 'relative',
    backgroundColor: 'orange',
    textDecorationColor: 'white',
    shadowColor: 'orange',
    padding: 5,
    margin: 10,
  },
  button: {
    padding: 5,
    margin: 10,
    fontFamily: 'Arial',
    
    
  }
});

export default App;
